class EthiopiaMiniMaxSearch:
    def __init__(self, graph, utilities, initial_state, depth=3):
        """
        graph: adjacency list {city: [neighbors]}
        utilities: terminal utility values {city: coffee_quality_score}
        initial_state: starting city
        depth: search depth limit
        """
        self.graph = graph
        self.utilities = utilities
        self.initial_state = initial_state
        self.depth = depth

    def minimax(self, state, depth, is_maximizing):
        # Base case: depth limit or terminal state
        if depth == 0 or state not in self.graph or state in self.utilities:
            return self.utilities.get(state, 0), [state]

        if is_maximizing:  # Agent's turn
            best_value = float("-inf")
            best_path = []
            for neighbor in self.graph[state]:
                value, path = self.minimax(neighbor, depth - 1, False)
                if value > best_value:
                    best_value = value
                    best_path = [state] + path
            return best_value, best_path
        else:  # Adversary's turn
            worst_value = float("inf")
            worst_path = []
            for neighbor in self.graph[state]:
                value, path = self.minimax(neighbor, depth - 1, True)
                if value < worst_value:
                    worst_value = value
                    worst_path = [state] + path
            return worst_value, worst_path

    def search(self):
        value, path = self.minimax(self.initial_state, self.depth, True)
        return path, value

# Utilities: coffee quality scores at terminal nodes
utilities = {
    "Shambu": 4,
    "Fincha": 5,
    "Gimbi": 8,
    "Limu": 8,
    "Hossana": 6,
    "Durame": 5,
    "Bench Naji": 5,
    "Tepi": 6,
    "Kaffa": 7,
    "Dilla": 9,
    "Chiro": 6,
    "Harar": 10
}

# Graph structure (simplified example)
graph = {
    "Addis Ababa": ["Shambu", "Hossana", "Chiro"],
    "Shambu": ["Fincha", "Gimbi"],
    "Hossana": ["Durame", "Bench Naji"],
    "Bench Naji": ["Tepi", "Kaffa"],
    "Chiro": ["Dilla", "Harar"],
    "Fincha": [],
    "Gimbi": [],
    "Limu": [],
    "Durame": [],
    "Tepi": [],
    "Kaffa": [],
    "Dilla": [],
    "Harar": []
}

# New: safe DFS that returns traversal order
def dfs(graph, start):
    stack = [start]
    visited = set()
    order = []
    while stack:
        city = stack.pop()
        if city not in visited:
            order.append(city)
            visited.add(city)
            for n in reversed(graph.get(city, [])):  # reversed to preserve expected order
                if n not in visited:
                    stack.append(n)
    return order

# New: safe BFS that returns traversal order
from collections import deque
def bfs(graph, start):
    queue = deque([start])
    visited = set()
    order = []
    while queue:
        city = queue.popleft()
        if city not in visited:
            order.append(city)
            visited.add(city)
            for n in graph.get(city, []):
                if n not in visited:
                    queue.append(n)
    return order

# New: add or extend neighbors for a city; ensures neighbor nodes exist
def add_city_neighbors(graph, city, neighbors, overwrite=False):
    if overwrite or city not in graph:
        graph[city] = list(neighbors)
    else:
        for n in neighbors:
            if n not in graph[city]:
                graph[city].append(n)
    for n in neighbors:
        graph.setdefault(n, [])
    return graph

# New: generator for stepwise expansion: yields (city, neighbors, graph_snapshot)
def expand_graph_stepwise(graph, steps):
    for city, neighbors in steps:
        add_city_neighbors(graph, city, neighbors)
        yield city, neighbors, dict(graph)  # shallow copy snapshot

# New: build graph from a full mapping (validates and ensures nodes exist)
def build_graph(mapping):
    new_graph = {}
    for city, neighbors in mapping.items():
        new_graph[city] = list(neighbors)
    for neighbors in mapping.values():
        for n in neighbors:
            new_graph.setdefault(n, [])
    return new_graph

import os
import re
import math
try:
    from rclpy.node import Node
    import rclpy
    from std_msgs.msg import String
    # new imports for nav path
    from nav_msgs.msg import Path
    from geometry_msgs.msg import PoseStamped
    ROS_AVAILABLE = True
except Exception:
    ROS_AVAILABLE = False

def build_graph_from_world(world_path, threshold=3.0):
    """Parse an SDF world and connect models whose XY distance <= threshold (meters).
    Fails with FileNotFoundError if world_path doesn't exist."""
    if not os.path.isfile(world_path):
        raise FileNotFoundError(f"World file not found: {world_path}")
    text = ""
    with open(world_path, "r", encoding="utf-8") as f:
        text = f.read()
    models = {}
    for m in re.finditer(r'<model\s+name="([^"]+)">(.*?)</model>', text, re.DOTALL):
        name = m.group(1)
        block = m.group(2)
        pose_match = re.search(r'<pose>([\s\S]*?)</pose>', block)
        if pose_match:
            parts = pose_match.group(1).strip().split()
            if len(parts) >= 3:
                x, y, z = float(parts[0]), float(parts[1]), float(parts[2])
                models[name] = (x, y, z)
    # build adjacency by proximity
    graph_out = {n: [] for n in models}
    names = list(models.keys())
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            xa, ya, _ = models[a]
            xb, yb, _ = models[b]
            if math.hypot(xa - xb, ya - yb) <= threshold:
                graph_out[a].append(b)
                graph_out[b].append(a)
    return graph_out, models

def find_path_bfs(graph, start, goal):
    """Uninformed BFS that returns the shortest unweighted path list or None."""
    if start not in graph or goal not in graph:
        return None
    from collections import deque
    q = deque([start])
    parent = {start: None}
    while q:
        node = q.popleft()
        if node == goal:
            path = []
            cur = goal
            while cur is not None:
                path.append(cur)
                cur = parent[cur]
            return list(reversed(path))
        for nb in graph.get(node, []):
            if nb not in parent:
                parent[nb] = node
                q.append(nb)
    return None

# New helper: normalize node names for robust matching
def _normalize_name(s: str) -> str:
    # Lowercase and keep alphanumerics only for robust matching
    return re.sub(r'[^a-z0-9]', '', s.lower())

def _build_name_index(nodes):
    # Map normalized -> canonical name (first wins)
    idx = {}
    for n in nodes:
        idx[_normalize_name(n)] = n
        # also map common variants: spaces <-> underscores
        idx[_normalize_name(n.replace('_', ' '))] = n
        idx[_normalize_name(n.replace(' ', '_'))] = n
    return idx

# Add UninformedPlanner to encapsulate BFS and world loading
class UninformedPlanner:
    """Simple uninformed planner using BFS and proximity-based world parsing."""
    def __init__(self, graph=None, positions=None):
        self.graph = graph or {}
        self.positions = positions or {}
        self.name_index = _build_name_index(self.graph.keys())

    def load_world(self, world_file, threshold=3.0):
        """Populate graph and positions by parsing an SDF world file."""
        g, pos = build_graph_from_world(world_file, threshold)
        self.graph = g
        self.positions = pos
        self.name_index = _build_name_index(self.graph.keys())

    def _resolve(self, name):
        """Resolve a user-supplied name to a canonical node present in graph."""
        if name is None:
            return None
        if name in self.graph:
            return name
        norm = _normalize_name(name)
        return self.name_index.get(norm)

    def plan(self, start, goal):
        """Return (name_path_list, list_of_positions_or_None). Names are resolved."""
        start_c = self._resolve(start)
        goal_c = self._resolve(goal)
        if start_c is None or goal_c is None:
            # Return None and details for caller to generate a helpful message
            return None, None
        name_path = find_path_bfs(self.graph, start_c, goal_c)
        if name_path is None:
            return None, None
        if not self.positions:
            return name_path, None
        poses = [self.positions.get(n, (0.0, 0.0, 0.0)) for n in name_path]
        return name_path, poses

if ROS_AVAILABLE:
    class PathPlannerNode(Node):
        """ROS2 node: subscribe /plan_request (String 'start,goal'), publish /planned_path and /planned_path_nav."""
        def __init__(self, world_file=None, threshold=3.0):
            super().__init__("path_planner")
            # parameters (use .value for robustness across rclpy versions)
            default_world = world_file or os.path.join(os.path.dirname(__file__), "figure5_traveling.world")
            self.declare_parameter("world_file", default_world)
            self.declare_parameter("threshold", float(threshold))
            world_file = self.get_parameter("world_file").value
            threshold = self.get_parameter("threshold").value

            self.sub = self.create_subscription(String, "/plan_request", self._cb_request, 10)
            self.pub = self.create_publisher(String, "/planned_path", 10)
            self.pub_nav = self.create_publisher(Path, "/planned_path_nav", 10)

            # Use UninformedPlanner internally
            self.planner = UninformedPlanner()
            try:
                self.planner.load_world(world_file, threshold)
                self.graph = self.planner.graph
                self.positions = self.planner.positions
                self.get_logger().info(f"Loaded graph from {world_file} ({len(self.graph)} nodes)")
            except Exception as e:
                # Graceful fallback
                self.get_logger().warning(f"Could not load world '{world_file}': {e}; using embedded graph")
                self.planner.graph = graph  # fallback to embedded graph
                self.planner.positions = {}
                self.graph = self.planner.graph
                self.positions = {}

        def plan(self, start, goal):
            """Return (name_path_list, nav_msgs.Path or None)."""
            name_path, poses = self.planner.plan(start, goal)
            if name_path is None:
                return None, None
            if poses is None:
                return name_path, None
            nav = Path()
            nav.header.frame_id = "map"
            nav.header.stamp = self.get_clock().now().to_msg()
            for (node, (x, y, z)) in zip(name_path, poses):
                ps = PoseStamped()
                ps.header = nav.header
                ps.pose.position.x = float(x)
                ps.pose.position.y = float(y)
                ps.pose.position.z = float(z)
                nav.poses.append(ps)
            return name_path, nav

        def _cb_request(self, msg):
            payload = msg.data.strip()
            parts = [p.strip() for p in payload.split(",")]
            if len(parts) != 2:
                self.get_logger().error("plan_request must be 'start,goal'")
                return
            start, goal = parts
            name_path, nav_path = self.plan(start, goal)
            out = String()
            out.data = "NO_PATH" if name_path is None else "->".join(name_path)
            self.get_logger().info(f"Plan request {start}->{goal} => {out.data}")
            self.pub.publish(out)
            if nav_path is not None:
                self.pub_nav.publish(nav_path)

        # add a small synchronous helper for external calls
        def request_plan(self, start, goal):
            """Synchronous helper: returns (name_list or None, Path or None)."""
            return self.plan(start, goal)

# CLI/demo (works even if ROS not installed)
if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", help="start node name")
    parser.add_argument("--goal", help="goal node name")
    parser.add_argument("--world", default=os.path.join(os.path.dirname(__file__), "figure5_traveling.world"))
    parser.add_argument("--threshold", type=float, default=3.0)
    parser.add_argument("--ros", action="store_true", help="run as ROS2 node (requires rclpy)")
    parser.add_argument("--list", action="store_true", help="list available nodes (after loading world)")
    parser.add_argument("--demo", action="store_true", help="run a small demo plan (Addis_Ababa -> Dilla)")
    args = parser.parse_args()

    if args.ros and ROS_AVAILABLE:
        rclpy.init()
        node = PathPlannerNode(world_file=args.world, threshold=args.threshold)
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        node.destroy_node()
        rclpy.shutdown()
        sys.exit(0)
    else:
        # When running without ROS, use UninformedPlanner in the CLI/demo path
        planner = UninformedPlanner()
        try:
            planner.load_world(args.world, args.threshold)
        except Exception as e:
            # fallback to embedded graph if world can't be loaded
            print(f"Warning: could not load world '{args.world}': {e}. Using embedded graph.")
            planner.graph = graph
            planner.positions = {}
            planner.name_index = _build_name_index(planner.graph.keys())

        if args.list:
            print("Available nodes:")
            for n in sorted(planner.graph.keys()):
                print(" ", n)
            sys.exit(0)
        if args.demo:
            start, goal = "Addis Ababa", "Dilla"
            p, poses = planner.plan(start, goal)
            if p:
                print("Demo plan:", " -> ".join(p))
                if poses:
                    print("Pose list:")
                    for n, (x, y, z) in zip(p, poses):
                        print(f"  {n}: ({x}, {y}, {z})")
                sys.exit(0)
            else:
                print(f"Demo: no path found from {start} to {goal}")
                sys.exit(1)

        if args.start and args.goal:
            p, poses = planner.plan(args.start, args.goal)
            if p:
                print("Planned path:", " -> ".join(p))
                if poses:
                    print("Pose list:")
                    for n, (x, y, z) in zip(p, poses):
                        print(f"  {n}: ({x}, {y}, {z})")
                sys.exit(0)
            else:
                # Try to give helpful feedback about unresolved names
                start_r = planner._resolve(args.start)
                goal_r = planner._resolve(args.goal)
                if start_r is None:
                    print(f"Start node '{args.start}' not found. Use --list to see available nodes.")
                if goal_r is None:
                    print(f"Goal node '{args.goal}' not found. Use --list to see available nodes.")
                if start_r and goal_r:
                    print(f"No path found from '{start_r}' to '{goal_r}'")
                sys.exit(2)
        else:
            print("Graph nodes sample:", list(planner.graph.keys())[:30])
            print("Use --start and --goal, or --list, or --demo for a quick example.")
            sys.exit(0)

