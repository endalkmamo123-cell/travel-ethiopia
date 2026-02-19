import sys
from unittest.mock import MagicMock

# Mock rclpy
sys.modules['rclpy'] = MagicMock()
sys.modules['rclpy.node'] = MagicMock()
sys.modules['geometry_msgs'] = MagicMock()
sys.modules['geometry_msgs.msg'] = MagicMock()

# Now import the search node
from .ethiopia_search import EthiopiaSearchNode
from .ethiopia_graph import ETHIOPIA_GRAPH

# Initialize node manually without calling super init (since we mocked the base class)
# But wait, python mocks might not behave like real classes for inheritance unless setup right.
# Let's just create a simpler test that instantiates the class.
# If `Node` is mocked, `EthiopiaSearchNode` inheriting from it should work.

node = EthiopiaSearchNode()

# Manually inject the graph if __init__ failed (but with mocks it should pass)
# The __init__ sets self.graph = ETHIOPIA_GRAPH
print("Graph keys:", len(node.graph.keys()))

assert node.graph == ETHIOPIA_GRAPH
print("Graph structure matches exactly.")

path = node.bfs_find_path('Gambella', 'Gode')
print(f"Path from Gambella to Gode: {path}")

# Verify path validity
assert path[0] == 'Gambella'
assert path[-1] == 'Gode'
for i in range(len(path)-1):
    u, v = path[i], path[i+1]
    assert v in node.graph[u], f"Invalid edge: {u} -> {v}"

print("Path verification PASSED.")

