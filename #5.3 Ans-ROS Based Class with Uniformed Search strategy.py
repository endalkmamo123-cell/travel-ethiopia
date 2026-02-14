#!/usr/bin/env python3
import sys
import argparse
import time
from collections import deque

# Try to import ROS packages; if unavailable run in a fallback CLI mode
try:
    import rclpy
    from rclpy.node import Node
    from geometry_msgs.msg import Twist
    HAS_ROS = True
except Exception:
    HAS_ROS = False

    # Lightweight compatibility shim for Twist when ROS is missing
    class Twist:
        def __init__(self):
            self.linear = type('L', (), {'x': 0.0})()
            self.angular = type('A', (), {'z': 0.0})()

# Node base: real ROS Node when available, else plain object
NodeBase = Node if HAS_ROS else object

# Full (unweighted) Figure 5 graph. Names use underscores to match the world file.
FIGURE5_GRAPH = {
    "Addis_Ababa": ["Debre_Birhan", "Adama", "Ambo"],
    "Debre_Birhan": ["Debre_Sina", "Addis_Ababa"],
    "Adama": ["Addis_Ababa", "Debre_Birhan", "Matahara", "Assela", "Batu"],
    "Ambo": ["Nekemte", "Addis_Ababa", "Wolkite"],
    "Matahara": ["Adama", "Awash"],
    "Awash": ["Chiro", "Kemise", "Matahara", "Dire_Dawa"],
    "Gabi_Rasu": ["Awash", "Samara"],
    "Samara": ["Gabi_Rasu", "Fanti_Rasu"],
    "Fanti_Rasu": ["Samara", "Kilbert_Rasu"],
    "Kilbert_Rasu": ["Fanti_Rasu"],
    "Debre_Sina": ["Kemise", "Debre_Birhan", "Debre_Markos"],
    "Kemise": ["Dessie", "Debre_Sina"],
    "Dessie": ["Woldia", "Kemise"],
    "Woldia": ["Alamata", "Dessie", "Semera"],
    "Alamata": ["Sekota", "Woldia", "Semera", "Mekelle"],
    "Sekota": ["Lalibela", "Alamata", "Mekelle"],
    "Lalibela": ["Debre_Tabor", "Sekota", "Woldia"],
    "Debre_Tabor": ["Bahir_Dar", "Lalibela"],
    "Bahir_Dar": ["Azezo", "Debre_Tabor", "Metekel", "Injubara", "Finote_Selam"],
    "Injubara": ["Bahir_Dar", "Finote_Selam"],
    "Finote_Selam": ["Bahir_Dar", "Injubara", "Debre_Markos"],
    "Debre_Markos": ["Debre_Sina", "Finote_Selam"],
    "Azezo": ["Gondar", "Bahir_Dar", "Metema"],
    "Gondar": ["Debark", "Metema", "Azezo", "Humera"],
    "Debark": ["Gondar", "Shire"],
    "Metema": ["Gondar", "Azezo", "Khartoum"],
    "Axum": ["Shire", "Adwa", "Asmra"],
    "Adigrat": ["Adwa", "Mekelle", "Asmra"],
    "Adwa": ["Mekelle", "Adigrat", "Axum"],
    "Shire": ["Humera", "Axum", "Debark"],
    "Humera": ["Shire", "Khartoum"],
    "Khartoum": ["Humera"],
    "Nekemte": ["Gimbi", "Ambo", "Bedelle"],
    "Gimbi": ["Dembi_Dollo", "Nekemte"],
    "Dembi_Dollo": ["Assosa", "Gimbi", "Gambela"],
    "Assosa": ["Dembi_Dollo", "Metekel"],
    "Metekel": ["Bahir_Dar", "Assosa"],
    "Jimma": ["Addis_Ababa", "Bedelle", "Bonga", "Wolkite"],
    "Bedelle": ["Jimma", "Gore", "Nekemte"],
    "Gore": ["Bedelle", "Gambela", "Tepi"],
    "Gambela": ["Gore", "Dembi_Dollo"],
    "Bonga": ["Jimma", "Mizan_Teferi", "Tepi", "Dawro"],
    "Mizan_Teferi": ["Bonga", "Tepi", "Basketo"],
    "Tepi": ["Mizan_Teferi", "Gore", "Bonga"],
    "Basketo": ["Arbaminich", "Dawro", "Mizan_Teferi", "Bench_Maji"],
    "Juba": ["Bench_Maji"],
    "Bench_Maji": ["Juba", "Basketo"],
    "Dawro": ["Basketo", "Bonga", "Wolaita_Sodo"],
    "Shashemene": ["Batu", "Hawassa", "Dodolla", "Hossana"],
    "Hawassa": ["Shashemene", "Dilla"],
    "Wolaita_Sodo": ["Dawro", "Hossana", "Arbaminich"],
    "Arbaminich": ["Wolaita_Sodo", "Basketo", "Konso"],
    "Konso": ["Arbaminich", "Yabelo"],
    "Hossana": ["Shashemene", "Wolaita_Sodo", "Worabe", "Jimma"],
    "Butajira": ["Batu", "Worabe"],
    "Batu": ["Shashemene", "Adama", "Butajira"],
    "Worabe": ["Hossana", "Butajira", "Wolkite"],
    "Wolkite": ["Worabe", "Ambo", "Bonga"],
    "Dilla": ["Hawassa", "Bule_Hora"],
    "Bule_Hora": ["Dilla", "Yabelo"],
    "Yabelo": ["Bule_Hora", "Moyale", "Konso"],
    "Moyale": ["Yabelo", "Nairobi"],
    "Nairobi": ["Moyale"],
    "Liben": ["Bale"],
    "Goba": ["Dega_Habur", "Sof_Oumer", "Bale"],
    "Bale": ["Goba", "Dodolla", "Liben", "Sof_Oumer"],
    "Dodolla": ["Shashemene", "Bale", "Assasa"],
    "Assasa": ["Assela", "Dodolla"],
    "Sof_Oumer": ["Bale", "Goba", "Kebri_Dehar"],
    "Gode": ["Dolo", "Kebri_Dehar"],
    "Dolo": ["Gode"],
    "Kebri_Dehar": ["Gode", "Warder"],
    "Warder": ["Kebri_Dehar"],
    "Dega_Habur": ["Warder", "Jijiga", "Goba", "Kebri_Dehar"],
    "Jijiga": ["Dega_Habur", "Babile"],
    "Babile": ["Harar", "Jijiga"],
    "Harar": ["Jijiga", "Dire_Dawa"],
    "Dire_Dawa": ["Harar", "Chiro"],
    "Chiro": ["Dire_Dawa", "Awash"],
}


def _normalize(name: str) -> str:
    """Normalize a city name to the underscore style used in the graph."""
    return name.strip().replace(" ", "_")


class EthiopiaSearchNode(NodeBase):
    def __init__(self, start=None, goal=None, strategy=None):
        # Only call ROS Node initializer when rclpy is available
        if HAS_ROS:
            super().__init__('ethiopia_search_node')
            # publisher only exists in ROS mode
            self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

            # ROS parameters: start, goal, strategy
            self.declare_parameter('start', 'Addis_Ababa')
            self.declare_parameter('goal', 'Axum')
            self.declare_parameter('strategy', 'BFS')

            start = _normalize(self.get_parameter('start').get_parameter_value().string_value)
            goal = _normalize(self.get_parameter('goal').get_parameter_value().string_value)
            self.strategy = self.get_parameter('strategy').get_parameter_value().string_value.upper()
        else:
            # CLI fallback: accept values passed into constructor or from argv
            self.publisher = None
            if start is None and goal is None and strategy is None:
                parser = argparse.ArgumentParser(description='Run Ethiopia search (fallback, no ROS)')
                parser.add_argument('--start', default='Addis_Ababa')
                parser.add_argument('--goal', default='Axum')
                parser.add_argument('--strategy', default='BFS')
                args = parser.parse_args()
                start = args.start
                goal = args.goal
                strategy = args.strategy
            self.strategy = (strategy or 'BFS').upper()

            start = _normalize(start)
            goal = _normalize(goal)

        # choose graph (FIGURE5_GRAPH has underscore names)
        self.graph = FIGURE5_GRAPH
        self.initial_state = start
        self.goal_state = goal

        # Validate
        if self.initial_state not in self.graph or self.goal_state not in self.graph:
            if HAS_ROS:
                self.get_logger().error(f"Start ({self.initial_state}) or goal ({self.goal_state}) not in Figure 5 graph")
                rclpy.shutdown()
            else:
                print(f"Error: Start ({self.initial_state}) or goal ({self.goal_state}) not in Figure 5 graph", file=sys.stderr)
            return

        # Compute path using selected strategy
        if self.strategy == 'BFS':
            self.path = self.bfs(self.initial_state, self.goal_state)
        elif self.strategy == 'DFS':
            self.path = self.dfs(self.initial_state, self.goal_state)
        else:
            msg = "Unsupported strategy; use 'BFS' or 'DFS'"
            if HAS_ROS:
                self.get_logger().error(msg)
                rclpy.shutdown()
            else:
                print(msg, file=sys.stderr)
            return

        if HAS_ROS:
            self.get_logger().info(f"Strategy={self.strategy}, Computed path: {self.path}")
        else:
            print(f"Strategy={self.strategy}, Computed path: {self.path}")

        # Timer to simulate robot movement along path (ROS: timer; fallback: none)
        self.index = 0
        if HAS_ROS:
            self.timer = self.create_timer(1.0, self.move_step)

    def bfs(self, start, goal):
        if start == goal:
            return [start]
        visited = {start}
        queue = deque([(start, [start])])
        while queue:
            node, path = queue.popleft()
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if neighbor == goal:
                        return path + [neighbor]
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def dfs(self, start, goal):
        if start == goal:
            return [start]
        visited = {start}
        stack = [(start, [start])]
        while stack:
            node, path = stack.pop()
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if neighbor == goal:
                        return path + [neighbor]
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))
        return None

    def _publish(self, msg: Twist):
        """Publish a Twist: use ROS publisher when available, else print a summary."""
        if HAS_ROS and self.publisher is not None:
            self.publisher.publish(msg)
        else:
            print(f"[publish] linear.x={msg.linear.x:.2f} angular.z={msg.angular.z:.2f}")

    def move_step(self):
        if self.path and self.index < len(self.path):
            current_city = self.path[self.index]
            if HAS_ROS:
                self.get_logger().info(f"Robot moving to: {current_city}")
            else:
                print(f"Robot moving to: {current_city}")

            # Publish a simple forward Twist message to simulate motion
            msg = Twist()
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self._publish(msg)

            self.index += 1
        else:
            if HAS_ROS:
                self.get_logger().info("Goal reached or no path available")
                self.destroy_timer(self.timer)
            else:
                print("Goal reached or no path available")

    def run_cli(self, delay: float = 1.0):
        """Run the path execution loop in non-ROS mode (blocking)."""
        if not self.path:
            print("No path to execute")
            return
        while self.index < len(self.path):
            self.move_step()
            time.sleep(delay)

def main(args=None):
    if HAS_ROS:
        rclpy.init(args=args)
        node = EthiopiaSearchNode()
        try:
            rclpy.spin(node)
        finally:
            node.destroy_node()
            rclpy.shutdown()
    else:
        # Fallback CLI mode: parse argv and run
        parser = argparse.ArgumentParser(description='Ethiopia search (fallback, no ROS)')
        parser.add_argument('--start', default='Addis_Ababa')
        parser.add_argument('--goal', default='Axum')
        parser.add_argument('--strategy', default='BFS')
        parser.add_argument('--step-delay', type=float, default=1.0, help='seconds between steps')
        parsed = parser.parse_args()

        node = EthiopiaSearchNode(start=parsed.start, goal=parsed.goal, strategy=parsed.strategy)
        node.run_cli(delay=parsed.step_delay)


if __name__ == '__main__':
    main()
