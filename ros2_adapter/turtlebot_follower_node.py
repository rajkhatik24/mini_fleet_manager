import math
import rclpy

from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy, ReliabilityPolicy

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry, Path


class TurtleBotFollower(Node):
    def __init__(self):
        super().__init__("turtlebot_follower_node")

        self.path = []
        self.current_index = 0
        self.last_path_signature = None

        self.x = 0.0
        self.y = 0.0
        self.yaw = 0.0

        self.has_odom = False
        self.has_path = False

        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)

        self.create_subscription(
            Odometry,
            "/odom",
            self.odom_callback,
            10,
        )

        path_qos = QoSProfile(depth=1)
        path_qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        path_qos.reliability = ReliabilityPolicy.RELIABLE

        self.create_subscription(
            Path,
            "/planned_path",
            self.path_callback,
            path_qos,
        )

        self.timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info("Follower started. Waiting for /odom and /planned_path.")

    def path_callback(self, msg):
        new_path = [
            (pose.pose.position.x, pose.pose.position.y)
            for pose in msg.poses
        ]

        signature = tuple(new_path)

        if signature != self.last_path_signature:
            self.path = new_path
            self.current_index = 0
            self.last_path_signature = signature
            self.has_path = True

            self.get_logger().info(f"Received new path with {len(self.path)} waypoints.")

    def odom_callback(self, msg):
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation
        self.yaw = self.quaternion_to_yaw(q.x, q.y, q.z, q.w)

        if not self.has_odom:
            self.get_logger().info("Odometry received.")

        self.has_odom = True

    def control_loop(self):
        cmd = Twist()

        if not self.has_odom or not self.has_path:
            self.cmd_pub.publish(cmd)
            return

        if self.current_index >= len(self.path):
            self.cmd_pub.publish(cmd)
            return

        target_x, target_y = self.path[self.current_index]

        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)

        target_yaw = math.atan2(dy, dx)
        yaw_error = self.normalize_angle(target_yaw - self.yaw)

        if distance < 0.15:
            self.get_logger().info(
                f"Reached waypoint {self.current_index}: ({target_x:.2f}, {target_y:.2f})"
            )
            self.current_index += 1
            return

        if abs(yaw_error) > 0.25:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.8 * yaw_error
        else:
            cmd.linear.x = min(0.22, distance)
            cmd.angular.z = 0.8 * yaw_error

        self.cmd_pub.publish(cmd)

    @staticmethod
    def quaternion_to_yaw(x, y, z, w):
        siny_cosp = 2.0 * (w * z + x * y)
        cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
        return math.atan2(siny_cosp, cosy_cosp)

    @staticmethod
    def normalize_angle(angle):
        while angle > math.pi:
            angle -= 2.0 * math.pi
        while angle < -math.pi:
            angle += 2.0 * math.pi
        return angle


def main(args=None):
    rclpy.init(args=args)
    node = TurtleBotFollower()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()