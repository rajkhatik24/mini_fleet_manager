import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy, ReliabilityPolicy

from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped


class PathPublisher(Node):
    def __init__(self):
        super().__init__("mini_fleet_path_publisher")

        qos = QoSProfile(depth=1)
        qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
        qos.reliability = ReliabilityPolicy.RELIABLE

        self.publisher = self.create_publisher(Path, "/planned_path", qos)

        self.path_points = [
            (0.0, 0.0),
            (1.0, 0.0),
            (2.0, 0.0),
            (2.0, 1.0),
            (2.0, 2.0),
            (1.0, 2.0),
            (0.0, 2.0),
        ]

        self.timer = self.create_timer(1.0, self.publish_path)

        self.get_logger().info("Path publisher started. Publishing /planned_path every 1 second.")

    def publish_path(self):
        path_msg = Path()
        path_msg.header.stamp = self.get_clock().now().to_msg()
        path_msg.header.frame_id = "odom"

        for x, y in self.path_points:
            pose = PoseStamped()
            pose.header = path_msg.header
            pose.pose.position.x = x
            pose.pose.position.y = y
            pose.pose.position.z = 0.0
            pose.pose.orientation.w = 1.0
            path_msg.poses.append(pose)

        self.publisher.publish(path_msg)
        self.get_logger().info(f"Published path with {len(path_msg.poses)} waypoints.")


def main(args=None):
    rclpy.init(args=args)
    node = PathPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()