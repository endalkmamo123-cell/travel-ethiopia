from collections import deque

graph = {
    "Addis Ababa": ["Debre Birhan", "Adama", "Ambo"],
    "Debre Birhan": ["Debre Sina", "Addis Ababa"],
    "Adama": ["Addis Ababa", "Debre Birhan", "Matahara", "Assela", "Batu"],
    "Ambo": ["Nekemte", "Addis Ababa", "Wolkite"],
    "Matahara": ["Adama", "Awash"],
    "Awash": ["Chiro", "Kemise", "Matahara", "Dire Dawa"],
    "Gabi Rasu": ["Awash", "Samara"],
    "Samara": ["Gabi Rasu", "Fanti Rasu"],
    "Fanti Rasu": ["Samara", "Kilbert Rasu"],
    "Kilbert Rasu": ["Fanti Rasu"],
    "Debre Sina": ["Kemise", "Debre Birhan", "Debre Markos"],
    "Kemise": ["Dessie", "Debre Sina"],
    "Dessie": ["Woldia", "Kemise"],
    "Woldia": ["Alamata", "Dessie", "Semera"],
    "Alamata": ["Sekota", "Woldia", "Semera", "Mekelle"],
    "Sekota": ["Lalibela", "Alamata", "Mekelle"],
    "Lalibela": ["Debre Tabor", "Sekota", "Woldia"],
    "Debre Tabor": ["Bahir Dar", "Lalibela"],
    "Bahir Dar": ["Azezo", "Debre Tabor", "Metekel", "Injubara", "Finote Selam"],
    "Injubara": ["Bahir Dar", "Finote Selam"],
    "Finote Selam": ["Bahir Dar", "Injubara", "Debre Markos"],
    "Debre Markos": ["Debre Sina", "Finote Selam"],
    "Azezo": ["Gondar", "Bahir Dar", "Metema"],
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
    "Gimbi": ["Dembi Dollo", "Nekemte"],
    "Dembi Dollo": ["Assosa", "Gimbi", "Gambela"],
    "Assosa": ["Dembi Dollo", "Metekel"],
    "Metekel": ["Bahir Dar", "Assosa"],
    "Jimma": ["Addis Ababa", "Bedelle", "Bonga", "Wolkite"],
    "Bedelle": ["Jimma", "Gore", "Nekemte"],
    "Gore": ["Bedelle", "Gambela", "Tepi"],
    "Gambela": ["Gore", "Dembi Dollo"],
    "Bonga": ["Jimma", "Mizan Teferi", "Tepi", "Dawro"],
    "Mizan Teferi": ["Bonga", "Tepi", "Basketo"],
    "Tepi": ["Mizan Teferi", "Gore", "Bonga"],
    "Basketo": ["Arbaminich", "Dawro", "Mizan Teferi", "Bench Maji"],
    "Juba": ["Bench Maji"],
    "Bench Maji": ["Juba", "Basketo"],
    "Dawro": ["Basketo", "Bonga", "Wolaita Sodo"],
    "Shashemene": ["Batu", "Hawassa", "Dodolla", "Hossana"],
    "Hawassa": ["Shashemene", "Dilla"],
    "Wolaita Sodo": ["Dawro", "Hossana", "Arbaminich"],
    "Arbaminich": ["Wolaita Sodo", "Basketo", "Konso"],
    "Konso": ["Arbaminich", "Yabelo"],
    "Hossana": ["Shashemene", "Wolaita Sodo", "Worabe", "Jimma"],
    "Butajira": ["Batu", "Worabe"],
    "Batu": ["Shashemene", "Adama", "Butajira"],
    "Worabe": ["Hossana", "Butajira", "Wolkite"],
    "Wolkite": ["Worabe", "Ambo", "Bonga"],
    "Dilla": ["Hawassa", "Bule Hora"],
    "Bule Hora": ["Dilla", "Yabelo"],
    "Yabelo": ["Bule Hora", "Moyale", "Konso"],
    "Moyale": ["Yabelo", "Nairobi"],
    "Nairobi": ["Moyale"],
    "Liben": ["Bale"],
    "Goba": ["Dega Habur", "Sof Oumer", "Bale"],
    "Bale": ["Goba", "Dodolla", "Liben", "Sof Oumer"],
    "Dodolla": ["Shashemene", "Bale", "Assasa"],
    "Assasa": ["Assela", "Dodolla"],
    "Sof Oumer": ["Bale", "Goba", "Kebri Dehar"],
    "Gode": ["Dolo", "Kebri Dehar"],
    "Dolo": ["Gode"],
    "Kebri Dehar": ["Gode", "Warder"],
    "Warder": ["Kebri Dehar"],
    "Dega Habur": ["Warder", "Jijiga", "Goba", "Kebri Dehar"],
    "Jijiga": ["Dega Habur", "Babile"],
    "Babile": ["Harar", "Jijiga"],
    "Harar": ["Jijiga", "Dire Dawa"],
    "Dire Dawa": ["Harar", "Chiro"],
    "Chiro": ["Dire Dawa", "Awash"]
}
class EthiopiaSearch:
    def __init__(self, graph, initial_state, goal_state, strategy="BFS"):
        self.graph = graph
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.strategy = strategy.upper()  # normalize input

    def search(self):
        if self.strategy == "BFS":
            return self._bfs()
        elif self.strategy == "DFS":
            return self._dfs()
        else:
            raise ValueError("Strategy must be either 'BFS' or 'DFS'")

    def _bfs(self):
        # trivial cases
        if self.initial_state == self.goal_state:
            return [self.initial_state]
        if self.initial_state not in self.graph or self.goal_state not in self.graph:
            return None

        visited = {self.initial_state}
        queue = deque([(self.initial_state, [self.initial_state])])

        while queue:
            node, path = queue.popleft()
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if neighbor == self.goal_state:
                        return path + [neighbor]
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None  # no path found

    def _dfs(self):
        # trivial cases
        if self.initial_state == self.goal_state:
            return [self.initial_state]
        if self.initial_state not in self.graph or self.goal_state not in self.graph:
            return None

        visited = {self.initial_state}
        stack = [(self.initial_state, [self.initial_state])]

        while stack:
            node, path = stack.pop()
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if neighbor == self.goal_state:
                        return path + [neighbor]
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

# BFS example
searcher = EthiopiaSearch(graph, "Addis Ababa", "Axum", strategy="BFS")
print("BFS Path:", searcher.search())

# DFS example
searcher = EthiopiaSearch(graph, "Addis Ababa", "Axum", strategy="DFS")
print("DFS Path:", searcher.search())


