#!/usr/bin/env python3

import socket
import struct

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


HOST = "127.0.0.1"
PORT = 15000


class CmdVelBridge(Node):

    def __init__(self):
        super().__init__("spot_cmd_vel_bridge")

        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM,
        )

        self.subscription = self.create_subscription(
            Twist,
            "/cmd_vel",
            self.cmd_vel_callback,
            10,
        )

        self.get_logger().info(
            f"Forwarding /cmd_vel to {HOST}:{PORT}"
        )

    def cmd_vel_callback(self, msg: Twist):

        vx = float(msg.linear.x)
        vy = float(msg.linear.y)
        wz = float(msg.angular.z)

        packet = struct.pack(
            "<fff",
            vx,
            vy,
            wz,
        )

        self.sock.sendto(
            packet,
            (HOST, PORT),
        )

        self.get_logger().info(
            f"cmd_vel: "
            f"vx={vx:+.2f}, "
            f"vy={vy:+.2f}, "
            f"wz={wz:+.2f}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = CmdVelBridge()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.sock.close()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
