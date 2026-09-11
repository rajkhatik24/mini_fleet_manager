from pathlib import Path
import time

import mujoco
import mujoco.viewer


SPOT_SCENE = (
    Path.home()
    / "projects"
    / "mujoco_menagerie"
    / "boston_dynamics_spot"
    / "scene.xml"
)


def main():
    print("Loading Spot:")
    print(SPOT_SCENE)

    if not SPOT_SCENE.exists():
        raise FileNotFoundError(
            f"Could not find Spot model at: {SPOT_SCENE}"
        )

    # Load MuJoCo model.
    model = mujoco.MjModel.from_xml_path(str(SPOT_SCENE))
    data = mujoco.MjData(model)

    print("\nModel loaded successfully.")
    print(f"nq          : {model.nq}")
    print(f"nv          : {model.nv}")
    print(f"nu          : {model.nu}")
    print(f"timestep    : {model.opt.timestep}")

    # Find Menagerie's predefined Spot standing/home pose.
    home_id = mujoco.mj_name2id(
        model,
        mujoco.mjtObj.mjOBJ_KEY,
        "home",
    )

    if home_id == -1:
        raise RuntimeError("Spot 'home' keyframe was not found.")

    # Reset both robot configuration AND actuator targets
    # to the Menagerie home state.
    mujoco.mj_resetDataKeyframe(
        model,
        data,
        home_id,
    )

    # Make sure derived state is updated.
    mujoco.mj_forward(model, data)

    print("\nLoaded Spot home keyframe.")
    print("Launching viewer...")

    with mujoco.viewer.launch_passive(model, data) as viewer:

        while viewer.is_running():

            step_start = time.time()

            # Advance physics.
            mujoco.mj_step(model, data)

            # Update viewer.
            viewer.sync()

            # Keep simulation approximately real-time.
            remaining = (
                model.opt.timestep
                - (time.time() - step_start)
            )

            if remaining > 0:
                time.sleep(remaining)


if __name__ == "__main__":
    main()