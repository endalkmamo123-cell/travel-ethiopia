import rclpy
from .ethiopia_search import EthiopiaSearchNode
from .ethiopia_graph import ETHIOPIA_GRAPH

def main(args=None):
    try:
        rclpy.init(args=args)
        node = EthiopiaSearchNode()
        
        print("Graph loaded keys:", len(node.graph.keys()))
        print("Expected keys:", len(ETHIOPIA_GRAPH.keys()))
        
        assert node.graph == ETHIOPIA_GRAPH
        print("Graph verification PASSED.")
        
        # Test path finding
        path = node.bfs_find_path('Gambella', 'Gode')
        print("Path found:", path)
        assert path is not None
        assert path[0] == 'Gambella'
        assert path[-1] == 'Gode'
        print("Path verification PASSED.")
        
        node.destroy_node()
        rclpy.shutdown()

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()

