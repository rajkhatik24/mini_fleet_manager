import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from visualization_msgs.msg import Marker, MarkerArray


class RobotStatePublisher(Node):
    def __init__(self, warehouse_map, frame_id: str = "map"):
        rclpy.init(args=None)

        super().__init__("mini_fleet_robot_state_publisher")

        self.warehouse_map = warehouse_map
        self.frame_id = frame_id

        self.marker_pub = self.create_publisher(
            MarkerArray,
            "/fleet/markers",
            10,
        )
    def _robot_color(self, robot_index):
        colors = [
            (0.0, 0.3, 1.0, 1.0),  # blue
            (1.0, 0.2, 0.2, 1.0),  # red
            (0.2, 1.0, 0.2, 1.0),  # green
            (1.0, 0.7, 0.0, 1.0),  # orange
            (0.8, 0.2, 1.0, 1.0),  # purple
        ]
        return colors[robot_index % len(colors)]

    def render(self, robots, tasks=None, current_tick: int = 0) -> None:
        markers = MarkerArray()

        delete_marker = Marker()
        delete_marker.action = Marker.DELETEALL
        markers.markers.append(delete_marker)

        marker_id = 0

        marker_id = self._add_warehouse_floor(
            markers,
            marker_id
        )
        marker_id = self._add_obstacles(markers, marker_id)
        marker_id = self._add_named_points(
            markers,
            marker_id,
            self.warehouse_map.pickup_points,
            "pickups",
            (0.0, 1.0, 0.0, 1.0),
        )
        marker_id = self._add_named_points(
            markers,
            marker_id,
            self.warehouse_map.dropoff_points,
            "dropoffs",
            (1.0, 0.0, 0.0, 1.0),
        )
        marker_id = self._add_named_points(
            markers,
            marker_id,
            self.warehouse_map.charging_stations,
            "chargers",
            (1.0, 0.5, 0.0, 1.0),
        )
        marker_id = self._add_robots(markers, marker_id, robots)
        marker_id = self._add_robot_labels(markers, marker_id, robots)
        marker_id = self._add_planned_routes(markers, marker_id, robots)

        self.marker_pub.publish(markers)
        rclpy.spin_once(self, timeout_sec=0.01)

    def _add_warehouse_floor(self, markers, marker_id):
        marker = Marker()

        marker.header.frame_id = self.frame_id
        marker.header.stamp = self.get_clock().now().to_msg()

        marker.ns = "warehouse_floor"
        marker.id = marker_id

        marker.type = Marker.CUBE
        marker.action = Marker.ADD

        marker.pose.position.x = (
            self.warehouse_map.width - 1
        ) / 2.0

        marker.pose.position.y = (
            self.warehouse_map.height - 1
        ) / 2.0

        marker.pose.position.z = -0.05

        marker.pose.orientation.w = 1.0

        marker.scale.x = float(self.warehouse_map.width - 1)
        marker.scale.y = float(self.warehouse_map.height - 1)
        marker.scale.z = 0.02

        marker.color.r = 0.25
        marker.color.g = 0.25
        marker.color.b = 0.25
        marker.color.a = 0.15

        markers.markers.append(marker)

        return marker_id + 1

    def _add_obstacles(self, markers, marker_id):
        for position in self.warehouse_map.obstacles:
            marker = self._make_cube(
                marker_id,
                "obstacles",
                position,
                z=0.05,
                scale=(0.9, 0.9, 0.1),
                color=(0.1, 0.1, 0.1, 1.0),
            )
            markers.markers.append(marker)
            marker_id += 1

        return marker_id

    def _add_named_points(self, markers, marker_id, points, namespace, color):
        for name, position in points.items():
            cube = self._make_cube(
                marker_id,
                namespace,
                position,
                z=0.05,
                scale=(0.75, 0.75, 0.08),
                color=color,
            )
            markers.markers.append(cube)
            marker_id += 1

            label = self._make_text(
                marker_id,
                f"{namespace}_labels",
                position,
                text=name,
                z=0.35,
                color=(1.0, 1.0, 1.0, 1.0),
            )
            markers.markers.append(label)
            marker_id += 1

        return marker_id

    def _add_robots(self, markers, marker_id, robots):
        for index, robot in enumerate(robots):
            marker = Marker()
            marker.header.frame_id = self.frame_id
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "robots"
            marker.id = marker_id
            marker.type = Marker.CYLINDER
            marker.action = Marker.ADD

            x, y = robot.position
            marker.pose.position.x = float(x)
            marker.pose.position.y = float(y)
            marker.pose.position.z = 0.35
            marker.pose.orientation.w = 1.0

            marker.scale.x = 0.75
            marker.scale.y = 0.75
            marker.scale.z = 0.35

            color = self._robot_color(index)
            marker.color.r = color[0]
            marker.color.g = color[1]
            marker.color.b = color[2]
            marker.color.a = color[3]

            markers.markers.append(marker)
            marker_id += 1

        return marker_id

    def _add_robot_labels(self, markers, marker_id, robots):
        for robot in robots:
            label = self._make_text(
                marker_id,
                "robot_labels",
                robot.position,
                text=str(robot.robot_id),
                z=0.85,
                color=(1.0, 1.0, 1.0, 1.0),
            )
            markers.markers.append(label)
            marker_id += 1

        return marker_id

    def _add_planned_routes(self, markers, marker_id, robots):
        for index, robot in enumerate(robots):
            if not robot.planned_route:
                continue

            marker = Marker()
            marker.header.frame_id = self.frame_id
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = "planned_routes"
            marker.id = marker_id
            marker.type = Marker.LINE_STRIP
            marker.action = Marker.ADD

            marker.pose.orientation.w = 1.0
            marker.scale.x = 0.08

            color = self._robot_color(index)
            marker.color.r = color[0]
            marker.color.g = color[1]
            marker.color.b = color[2]
            marker.color.a = 1.0

            for x, y in robot.planned_route:
                point = Point()
                point.x = float(x)
                point.y = float(y)
                point.z = 0.15
                marker.points.append(point)

            markers.markers.append(marker)
            marker_id += 1

        return marker_id

    def _make_cube(self, marker_id, namespace, position, z, scale, color):
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = namespace
        marker.id = marker_id
        marker.type = Marker.CUBE
        marker.action = Marker.ADD

        x, y = position
        marker.pose.position.x = float(x)
        marker.pose.position.y = float(y)
        marker.pose.position.z = z
        marker.pose.orientation.w = 1.0

        marker.scale.x = scale[0]
        marker.scale.y = scale[1]
        marker.scale.z = scale[2]

        marker.color.r = color[0]
        marker.color.g = color[1]
        marker.color.b = color[2]
        marker.color.a = color[3]

        return marker

    def _make_text(self, marker_id, namespace, position, text, z, color):
        marker = Marker()
        marker.header.frame_id = self.frame_id
        marker.header.stamp = self.get_clock().now().to_msg()
        marker.ns = namespace
        marker.id = marker_id
        marker.type = Marker.TEXT_VIEW_FACING
        marker.action = Marker.ADD

        x, y = position
        marker.pose.position.x = float(x)
        marker.pose.position.y = float(y)
        marker.pose.position.z = z
        marker.pose.orientation.w = 1.0

        marker.text = text
        marker.scale.z = 0.3

        marker.color.r = color[0]
        marker.color.g = color[1]
        marker.color.b = color[2]
        marker.color.a = color[3]

        return marker

    def close(self) -> None:
        self.destroy_node()
        rclpy.shutdown()