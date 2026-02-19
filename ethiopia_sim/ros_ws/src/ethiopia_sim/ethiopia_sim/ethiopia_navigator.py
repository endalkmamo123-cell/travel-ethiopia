import rclpy
import time
import math
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from collections import deque
from .ethiopia_graph import ETHIOPIA_GRAPH
from .city_coordiantes import CITY_COORDS

class EthiopiaNavigator(Node):
    def __init__(self):
        super().__init__('ethiopia_navigator')
        # Topics exposed by the Gazebo Sim DiffDrive plugin for model "ethiopia_bot"
        self.publisher_ = self.create_publisher(Twist, '/model/ethiopia_bot/cmd_vel', 10)
        self.odom_sub = self.create_subscription(Odometry, '/model/ethiopia_bot/odometry', self.odom_callback, 10)
        self.graph = ETHIOPIA_GRAPH
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0

    def odom_callback(self, msg):
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        
        # Quaternion to yaw
        q = msg.pose.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        self.current_yaw = math.atan2(siny_cosp, cosy_cosp)

    def bfs_find_path(self, start, goal):
        queue = deque([[start]])
        visited = {start}
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == goal:
                return path
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return None

    def move_to(self, x_goal, y_goal):
        twist = Twist()
        rate = self.create_rate(10)
        
        self.get_logger().info(f"Navigating to coordinate: ({x_goal}, {y_goal})")

        while rclpy.ok():
            dx = x_goal - self.current_x
            dy = y_goal - self.current_y
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < 0.2:
                break
            
            angle_to_goal = math.atan2(dy, dx)
            angle_diff = angle_to_goal - self.current_yaw
            
            # Normalize angle
            while angle_diff > math.pi: angle_diff -= 2 * math.pi
            while angle_diff < -math.pi: angle_diff += 2 * math.pi

            if abs(angle_diff) > 0.1:
                twist.linear.x = 0.0
                twist.angular.z = 0.5 if angle_diff > 0 else -0.5
            else:
                twist.linear.x = min(0.3, distance)
                twist.angular.z = 0.0
            
            self.publisher_.publish(twist)
            rclpy.spin_once(self, timeout_sec=0.01)
            # rate.sleep() # rate.sleep() is buggy in some rclpy versions, using spin_once with timeout instead

        twist.linear.x = 0.0
        twist.angular.z = 0.0
        self.publisher_.publish(twist)
        self.get_logger().info("Reached waypoint.")

    def travel_path(self, path):
        if not path:
            self.get_logger().error("No path found")
            return
        self.get_logger().info(f"Path Found: {' -> '.join(path)}")
        for city in path:
            self.get_logger().info(f"Moving to {city}")
            x, y = CITY_COORDS[city]
            self.move_to(x, y)
            time.sleep(1.0)

def main(args=None):
    rclpy.init(args=args)
    node = EthiopiaNavigator()
    
    # Wait for odom to start working
    node.get_logger().info("Waiting for odometry...")
    for _ in range(10):
        rclpy.spin_once(node, timeout_sec=0.5)
    
    start_city = "Gambella"
    goal_city = "Gode"
    
    path = node.bfs_find_path(start_city, goal_city)
    if path:
        node.travel_path(path)
    else:
        node.get_logger().error(f"Could not find path from {start_city} to {goal_city}")
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

