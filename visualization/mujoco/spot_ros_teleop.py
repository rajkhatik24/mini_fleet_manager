import argparse
import socket
import struct
import time

import jax
import jax.numpy as jp
import mujoco
import mujoco.viewer
import numpy as np

from brax.training.agents.ppo import checkpoint as ppo_checkpoint
from mujoco_playground import locomotion


UDP_HOST = "127.0.0.1"
UDP_PORT = 15000

COMMAND_TIMEOUT = 0.75


def apply_command(state, command):
    """Inject [vx, vy, yaw_rate] into Spot's policy state."""

    command = jp.asarray(
        command,
        dtype=jp.float32,
    )

    info = dict(state.info)
    info["command"] = command

    obs = dict(state.obs)

    # SpotFlatTerrainJoystick builds its state observation
    # with the command as the final 3 values.
    obs["state"] = (
        obs["state"]
        .at[-3:]
        .set(command)
    )

    return state.replace(
        info=info,
        obs=obs,
    )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--checkpoint",
        required=True,
    )

    args = parser.parse_args()

    # ---------------------------------------------------------
    # UDP command receiver
    # ---------------------------------------------------------

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_DGRAM,
    )

    sock.bind(
        (
            UDP_HOST,
            UDP_PORT,
        )
    )

    sock.setblocking(False)

    print(
        f"Listening for ROS velocity commands on "
        f"udp://{UDP_HOST}:{UDP_PORT}"
    )

    command = np.zeros(
        3,
        dtype=np.float32,
    )

    last_command_time = 0.0

    # ---------------------------------------------------------
    # Environment
    # ---------------------------------------------------------

    print("Loading SpotFlatTerrainJoystick...")

    env = locomotion.load(
        "SpotFlatTerrainJoystick",
        config_overrides={
            "impl": "jax",
        },
    )

    # ---------------------------------------------------------
    # Policy
    # ---------------------------------------------------------

    print("Loading checkpoint:")
    print(args.checkpoint)

    policy = ppo_checkpoint.load_policy(
        args.checkpoint,
        deterministic=True,
    )

    policy = jax.jit(policy)

    reset_fn = jax.jit(env.reset)
    step_fn = jax.jit(env.step)

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    rng = jax.random.PRNGKey(0)

    rng, reset_key = jax.random.split(rng)

    state = reset_fn(reset_key)

    # ---------------------------------------------------------
    # JIT warmup
    # ---------------------------------------------------------

    print("Compiling policy + simulation...")

    state = apply_command(
        state,
        np.zeros(3, dtype=np.float32),
    )

    rng, action_key = jax.random.split(rng)

    action, _ = policy(
        state.obs,
        action_key,
    )

    state = step_fn(
        state,
        action,
    )

    jax.block_until_ready(
        state.data.qpos
    )

    print("Compilation complete.")

    # Clean reset after compilation.
    rng, reset_key = jax.random.split(rng)

    state = reset_fn(reset_key)

    # ---------------------------------------------------------
    # Viewer
    # ---------------------------------------------------------

    mj_model = env.mj_model
    mj_data = mujoco.MjData(mj_model)

    mj_data.qpos[:] = np.asarray(
        state.data.qpos
    )

    mj_data.qvel[:] = np.asarray(
        state.data.qvel
    )

    mujoco.mj_forward(
        mj_model,
        mj_data,
    )

    print()
    print("====================================")
    print(" Spot ROS 2 Teleop")
    print("====================================")
    print("ROS /cmd_vel → UDP → PPO → MuJoCo")
    print("====================================")
    print()

    with mujoco.viewer.launch_passive(
        mj_model,
        mj_data,
    ) as viewer:

        try:

            body_id = mj_model.body(
                "body"
            ).id

            viewer.cam.type = (
                mujoco.mjtCamera.mjCAMERA_TRACKING
            )

            viewer.cam.trackbodyid = body_id
            viewer.cam.distance = 3.0
            viewer.cam.elevation = -20

        except Exception:
            print(
                "Tracking camera unavailable; "
                "continuing."
            )

        while viewer.is_running():

            loop_start = time.time()

            # -------------------------------------------------
            # Receive newest ROS command
            # -------------------------------------------------

            while True:

                try:

                    packet, _ = sock.recvfrom(
                        1024
                    )

                except BlockingIOError:
                    break

                if len(packet) != 12:
                    continue

                vx, vy, wz = struct.unpack(
                    "<fff",
                    packet,
                )

                # Clamp to Spot training distribution.
                command[:] = [
                    np.clip(
                        vx,
                        -1.0,
                        1.0,
                    ),
                    np.clip(
                        vy,
                        -0.8,
                        0.8,
                    ),
                    np.clip(
                        wz,
                        -1.0,
                        1.0,
                    ),
                ]

                last_command_time = (
                    time.monotonic()
                )

                print(
                    f"\rROS command | "
                    f"vx={command[0]:+.2f} "
                    f"vy={command[1]:+.2f} "
                    f"wz={command[2]:+.2f}",
                    end="",
                    flush=True,
                )

            # -------------------------------------------------
            # Dead-man timeout
            # -------------------------------------------------

            if (
                last_command_time == 0.0
                or
                time.monotonic()
                - last_command_time
                > COMMAND_TIMEOUT
            ):
                command[:] = 0.0

            # -------------------------------------------------
            # Apply velocity command
            # -------------------------------------------------

            state = apply_command(
                state,
                command,
            )

            # -------------------------------------------------
            # PPO inference
            # -------------------------------------------------

            rng, action_key = (
                jax.random.split(rng)
            )

            action, _ = policy(
                state.obs,
                action_key,
            )

            state = step_fn(
                state,
                action,
            )

            jax.block_until_ready(
                state.data.qpos
            )

            # -------------------------------------------------
            # Reset if Spot falls
            # -------------------------------------------------

            if bool(
                np.asarray(
                    state.done
                )
            ):

                print(
                    "\nSpot fell. Resetting."
                )

                rng, reset_key = (
                    jax.random.split(rng)
                )

                state = reset_fn(
                    reset_key
                )

                command[:] = 0.0
                last_command_time = 0.0

            # -------------------------------------------------
            # Sync MJX → regular MuJoCo viewer
            # -------------------------------------------------

            with viewer.lock():

                mj_data.qpos[:] = np.asarray(
                    state.data.qpos
                )

                mj_data.qvel[:] = np.asarray(
                    state.data.qvel
                )

                mj_data.time = float(
                    np.asarray(
                        state.data.time
                    )
                )

                mujoco.mj_forward(
                    mj_model,
                    mj_data,
                )

            viewer.sync()

            # 50 Hz locomotion controller.
            elapsed = (
                time.time() - loop_start
            )

            remaining = (
                env.dt - elapsed
            )

            if remaining > 0:
                time.sleep(remaining)

    sock.close()


if __name__ == "__main__":
    main()