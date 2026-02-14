import heapq
graph = {    
    "Addis Ababa": [("Debre Birhan", 3), ("Adama", 4), ("Ambo", 5)],
    "Debre Birhan": [("DebreSina", 3), ("Addis Ababa", 3)],
    "Adama": [("Addis Ababa", 4), ("Matahara", 4), ("Assela", 3), ("Batu", 3)],
    "Ambo": [("Nekemte", 4), ("Addis Ababa", 5), ("Wolkite", 4)],
    "Matahara": [("Adama", 4), ("Awash", 4)],
    "Awash": [("Chiro", 4), ("Kemise", 4), ("Matahara", 4), ("Dire Dawa", 4)],
    "Gabi Rasu": [("Awash", 4), ("Samara", 4)],
    "Samara": [("Gabi Rasu", 4), ("Fanti Rasu", 6)],
    "Fanti Rasu": [("Samara", 6), ("Kilbet Rasu", 6)],
    "Kilbet Rasu": [("Fanti Rasu", 6)],
    "Debre Sina": [("Kemise", 4), ("Debre Birhan", 3), ("Debre Markos", 17)],
    "Kemise": [("Dessie", 4), ("Debre Sina", 4)],
    "Dessie": [("Woldia", 6), ("Kemise", 4)],
    "Woldia": [("Alamata", 8), ("Dessie", 6), ("Semera", 8)],
    "Alamata": [("Sekota", 6), ("Woldia", 8), ("Mekelle", 6)],
    "Sekota": [("Lalibela", 4), ("Alamata", 6), ("Mekelle", 4)],
    "Lalibela": [("Debre Tabor", 8), ("Sekota", 4), ("Woldia", 8)],
    "Debre Tabor": [("Bahir Dar", 4), ("Lalibela", 8)],
    "Bahir Dar": [("Azezo", 4), ("Debre Tabor", 4), ("Metekel", 4), ("Injibara", 2), ("Finote Selam", 2)],
    "Injibara": [("Bahir Dar", 2), ("Finote Selam", 2)],
    "Finote Selam": [("Bahir Dar", 2), ("Injibara", 2), ("Debre Markos", 2)],
    "Debre Markos": [("Debre Sina", 17), ("Finote Selam", 2)],
    "Azezo": [("Gondar", 4), ("Bahir Dar", 4), ("Metema", 7)],
    "Gondar": [("Debark", 4), ("Metema", 7), ("Azezo", 4), ("Humera", 4)],
    "Debark": [("Gondar", 4), ("Shire", 6)],
    "Metema": [("Gondar", 7), ("Azezo", 7), ("Khartoum", 21)],
    "Axum": [("Shire", 4), ("Adwa", 3), ("Asmara", 10)],
    "Adigrat": [("Adwa", 3), ("Mekelle", 6), ("Asmara", 10)],
    "Adwa": [("Mekelle", 6), ("Adigrat", 3), ("Axum", 3)],
    "Shire": [("Humera", 6), ("Axum", 4), ("Debark", 6)],
    "Humera": [("Shire", 6), ("Khartoum", 21)],
    "Khartoum": [("Humera", 21), ("Metema", 21)],
    "Nekemte": [("Gimbi", 4), ("Ambo", 4), ("Bedele", 9)],
    "Gimbi": [("Dembi Dollo", 6), ("Nekemte", 4)],
    "Dembi Dollo": [("Assosa", 4), ("Gimbi", 6), ("Gambela", 6)],
    "Assosa": [("Dembi Dollo", 4), ("Metekel", 11)],
    "Metekel": [("Bahir Dar", 4), ("Assosa", 11)],
    "Jimma": [("Addis Ababa", 6), ("Bedele", 9), ("Bonga", 4), ("Wolkite", 4)],
    "Bedele": [("Jimma", 9), ("Gore", 9), ("Nekemte", 9)],
    "Gore": [("Bedele", 9), ("Gambela", 4), ("Tepi", 9)],
    "Gambela": [("Gore", 4), ("Dembi Dollo", 6)],
    "Bonga": [("Jimma", 4), ("Mizan Teferi", 4), ("Tepi", 4), ("Dawro", 4)],
    "Mizan Teferi": [("Bonga", 4), ("Tepi", 4), ("Basketo", 4)],
    "Tepi": [("Mizan Teferi", 4), ("Gore", 9), ("Bonga", 4)],
    "Basketo": [("Arba Minch", 4), ("Dawro", 4), ("Mizan Teferi", 4), ("Bench Maji", 10)],
    "Boma": [("Juba", 10), ("Bench Maji", 5)],
    "Juba": [("Bench Maji", 10)],
    "Bench Maji": [("Juba", 10), ("Basketo", 10)],
    "Dawro": [("Basketo", 4), ("Bonga", 4), ("Wolaita Sodo", 4)],
    "Shashamene": [("Batu", 4), ("Hawassa", 4), ("Dodola", 13), ("Hossana", 6)],
    "Dodola": [("Shashamene", 13), ("Bale", 13), ("Assasa", 3)],
    "Hossana": [("Shashamene", 6), ("Wolaita Sodo", 4), ("Worabe", 4), ("Jimma", 6)],
    "Hawassa": [("Shashamene", 4), ("Dilla", 3)],
    "Wolaita Sodo": [("Dawro", 4), ("Hossana", 4), ("Arba Minch", 3)],
    "Arba Minch": [("Wolaita Sodo", 3), ("Konso", 4)],
    "Konso": [("Arba Minch", 4), ("Yabelo", 3)],
    "Batu": [("Shashamene", 4), ("Adama", 3), ("Butajira", 4)],
    "Butajira": [("Batu", 4), ("Worabe", 4)],
    "Worabe": [("Hossana", 4), ("Butajira", 4), ("Wolkite", 4)],
    "Wolkite": [("Worabe", 4), ("Ambo", 4), ("Bonga", 4)],
    "Dilla": [("Hawassa", 3), ("Bule Hora", 4)],
    "Bule Hora": [("Dilla", 4), ("Yabelo", 5)],
    "Yabelo": [("Bule Hora", 5), ("Moyale", 6), ("Konso", 3)],
    "Moyale": [("Yabelo", 6), ("Nairobi", 22)],
    "Nairobi": [("Moyale", 22)],
    "Goba": [("Dega Habur", 18), ("Sof Oumer", 18), ("Bale", 28)],
    "Bale": [("Goba", 28), ("Dodola", 13), ("Liben", 23), ("Sof Oumer", 23)],
    "Assasa": [("Assela", 4), ("Dodola", 3)],
    "Sof Oumer": [("Bale", 23), ("Goba", 18), ("Kebri Dehar", 23)],
    "Gode": [("Dolo", 11), ("Kebri Dehar", 5), ("Mogadisho", 22)],
    "Dolo": [("Gode", 11)],
    "Kebri Dehar": [("Gode", 5), ("Warder", 6), ("Sof Oumer", 23), ("Dega Habur", 6)],
    "Warder": [("Kebri Dehar", 6), ("Dega Habur", 6)],
    "Dega Habur": [("Warder", 6), ("Jijiga", 5), ("Goba", 18), ("Kebri Dehar", 6)],
    "Jijiga": [("Dega Habur", 5), ("Babile", 5)],
    "Babile": [("Harar", 4), ("Jijiga", 5)],
    "Harar": [("Jijiga", 3), ("Dire Dawa", 4), ("Babile", 4)],
    "Dire Dawa": [("Harar", 4), ("Chiro", 4)],
    "Chiro": [("Dire Dawa", 4), ("Debre Birhan", 4)]
}

class AStarSearch:
    def __init__(self, graph, heuristics):
        """
        graph: dict mapping each node to list of (neighbor, cost)
        heuristics: dict mapping each node to heuristic value h(n)
        """
        self.graph = graph
        self.heuristics = heuristics

    def search(self, start, goal):
        # Use g_scores to avoid processing stale (worse) frontier entries
        frontier = [(self.heuristics.get(start, float("inf")), 0, [start])]
        g_scores = {start: 0}

        while frontier:
            f, g, path = heapq.heappop(frontier)
            current = path[-1]

            # Goal check
            if current == goal:
                return path, g

            # Skip outdated entry
            if g > g_scores.get(current, float("inf")):
                continue

            # Expand neighbors
            for neighbor, step_cost in self.graph.get(current, []):
                g_new = g + step_cost
                if g_new < g_scores.get(neighbor, float("inf")):
                    g_scores[neighbor] = g_new
                    f_new = g_new + self.heuristics.get(neighbor, float("inf"))
                    heapq.heappush(frontier, (f_new, g_new, path + [neighbor]))

        return None, float("inf")


heuristics = {
    "Addis Ababa": 13,
    "Debre Birhan": 12,
    "Debre Sina": 11,
    "Kemise": 10,
    "Dessie": 9,
    "Woldia": 8,
    "Alamata": 7,
    "Sekota": 6,
    "Lalibela": 5,
    "Moyale": 0   # Goal has h=0
    # ... (fill in other heuristic values from Figure 3)
}

# Run A* search
astar = AStarSearch(graph, heuristics)
path, cost = astar.search("Addis Ababa", "Moyale")

if path is None:
    print("No path found from Addis Ababa to Moyale")
else:
    print("Optimal Path:", " -> ".join(path))
    print("Total Cost:", cost)