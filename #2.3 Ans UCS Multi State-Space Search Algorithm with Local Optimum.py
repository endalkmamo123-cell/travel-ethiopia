import heapq
graph = {
    # Core hub
    "Addis Ababa": [("Debre Birhan", 3), ("Adama", 4), ("Ambo", 5)],
    # North corridor (to Lalibela, Gondar, Axum)
    "Debre Birhan": [("Debre Markos", 17), ("Chiro", 4), ("Addis Ababa", 3)],
    "Chiro": [("Dire Dawa", 4), ("Debre Birhan", 4)],
    "Dire Dawa": [("Harar", 4), ("Chiro", 4)],
    "Harar": [("Dire Dawa", 4), ("Babile", 4), ("Jijiga", 3)],
    "Babile": [("Harar", 4), ("Jijiga", 5)],
    "Jijiga": [("Babile", 5), ("Dega Habur", 5)],
    "Debre Markos": [("Finote Selam", 2), ("Debre Birhan", 17)],
    "Finote Selam": [("Debre Markos", 2), ("Injibara", 2), ("Bahir Dar", 2)],
    "Injibara": [("Finote Selam", 2), ("Bahir Dar", 2)],
    "Bahir Dar": [("Debre Tabor", 4), ("Azezo", 4), ("Metekel", 4), ("Injibara", 2), ("Finote Selam", 2)],
    "Debre Tabor": [("Bahir Dar", 4), ("Lalibela", 8)],
    "Lalibela": [("Debre Tabor", 8), ("Sekota", 4), ("Woldia", 8)],
    "Woldia": [("Dessie", 6), ("Alamata", 8)],
    "Dessie": [("Kemise", 4), ("Woldia", 6)],
    "Kemise": [("Debre Sina", 4), ("Dessie", 4)],
    "Debre Sina": [("Debre Birhan", 3), ("Kemise", 4), ("Debre Markos", 17)],
    "Azezo": [("Gondar", 4), ("Bahir Dar", 4), ("Metema", 7)],
    "Gondar": [("Azezo", 4), ("Debark", 4), ("Metema", 7), ("Humera", 4)],
    "Debark": [("Gondar", 4), ("Shire", 6)],
    "Shire": [("Debark", 6), ("Axum", 4), ("Humera", 6)],
    "Axum": [("Shire", 4), ("Adwa", 3), ("Asmara", 10)],
    "Adwa": [("Axum", 3), ("Adigrat", 3), ("Mekele", 6)],
    "Adigrat": [("Mekele", 6), ("Adwa", 3), ("Asmara", 10)],
    "Mekele": [("Kilbet Rasu", 6), ("Sekota", 4), ("Adigrat", 6)],
    "Sekota": [("Lalibela", 4), ("Alamata", 6), ("Mekele", 4)],
    "Alamata": [("Woldia", 8), ("Sekota", 6), ("Fanti Rasu", 6)],
    "Fanti Rasu": [("Kilbet Rasu", 6), ("Alamata", 6)],
    "Kilbet Rasu": [("Fanti Rasu", 6), ("Mekele", 6)],

    # Southwest corridor (to Jimma, Arba Minch)
    "Ambo": [("Addis Ababa", 5), ("Nekemte", 4), ("Wolkite", 4)],
    "Wolkite": [("Ambo", 4), ("Worabe", 4), ("Bonga", 4)],
    "Worabe": [("Wolkite", 4), ("Butajira", 4), ("Hossana", 4)],
    "Butajira": [("Batu", 4), ("Worabe", 4)],
    "Batu": [("Adama", 3), ("Shashamene", 4), ("Butajira", 4)],
    "Shashamene": [("Batu", 4), ("Hawassa", 4), ("Dodola", 13), ("Hossana", 6)],
    "Hawassa": [("Shashamene", 4), ("Dilla", 3)],
    "Dilla": [("Hawassa", 3), ("Bule Hora", 4)],
    "Bule Hora": [("Dilla", 4), ("Yabelo", 5)],
    "Yabelo": [("Bule Hora", 5), ("Konso", 3), ("Moyale", 6)],
    "Konso": [("Yabelo", 3), ("Arba Minch", 4)],
    "Arba Minch": [("Konso", 4), ("Wolaita Sodo", 3)],
    "Wolaita Sodo": [("Arba Minch", 3), ("Hossana", 4), ("Dawro", 4)],
    "Bonga": [("Wolkite", 4), ("Jimma", 4), ("Tepi", 4), ("Dawro", 4)],
    "Jimma": [("Bonga", 4), ("Bedele", 9), ("Wolkite", 4), ("Addis Ababa", 6)],
    "Bedele": [("Jimma", 9), ("Gore", 9), ("Nekemte", 9)],
    "Gore": [("Bedele", 9), ("Gambela", 4), ("Tepi", 9)],
    "Tepi": [("Bonga", 4), ("Mizan Teferi", 4), ("Gore", 9)],
    "Mizan Teferi": [("Bonga", 4), ("Tepi", 4), ("Basketo", 4)],
    "Dawro": [("Bonga", 4), ("Wolaita Sodo", 4), ("Basketo", 4)],
    "Basketo": [("Dawro", 4), ("Mizan Teferi", 4), ("Arba Minch", 4)],

    # Southeast corridor (to Bale, Sof Oumer)
    "Adama": [("Addis Ababa", 4), ("Matahara", 4), ("Assela", 3), ("Batu", 3)],
    "Matahara": [("Adama", 4), ("Awash", 4)],
    "Awash": [("Matahara", 4), ("Chiro", 4), ("Kemise", 4), ("Dire Dawa", 4)],
    "Assela": [("Adama", 3), ("Assasa", 4)],
    "Assasa": [("Assela", 4), ("Dodola", 3)],
    "Dodola": [("Assasa", 3), ("Bale", 13), ("Shashamene", 13)],
    "Bale": [("Dodola", 13), ("Goba", 28), ("Sof Oumer", 23), ("Liben", 23)],
    "Goba": [("Bale", 28), ("Sof Oumer", 18), ("Babile", 28)],
    "Sof Oumer": [("Bale", 23), ("Goba", 18), ("Kebri Dehar", 23)],
    "Kebri Dehar": [("Sof Oumer", 23), ("Warder", 6), ("Gode", 5), ("Dega Habur", 6)],
    "Warder": [("Kebri Dehar", 6), ("Dega Habur", 6)],
    "Dega Habur": [("Warder", 6), ("Kebri Dehar", 6), ("Jijiga", 5), ("Goba", 18)],
    "Gode": [("Kebri Dehar", 5), ("Sof Oumer", 23), ("Dolo", 11)],
    "Dolo": [("Gode", 11)]
}
def multi_goal_ucs(graph, start, goals):
    goals = frozenset(goals)
    # State: (current_city, visited_goals_frozenset)
    start_state = (start, frozenset([start]) & goals)

    # Priority queue of (cost, state, path)
    frontier = [(0, start_state, [start])]
    # Best known cost to a (city, visited_goals) state
    best = {start_state: 0}

    while frontier:
        cost, (city, visited), path = heapq.heappop(frontier)

        # Goal condition: all goals visited
        if visited == goals:
            return cost, path

        # Skip if we have already found a cheaper way to this state
        if cost > best[(city, visited)]:
            continue

        for nbr, w in graph.get(city, []):
            new_cost = cost + w
            new_visited = visited | (frozenset([nbr]) & goals)
            new_state = (nbr, new_visited)
            if new_state not in best or new_cost < best[new_state]:
                best[new_state] = new_cost
                heapq.heappush(frontier, (new_cost, new_state, path + [nbr]))

    return None  # No solution
goals = {"Axum", "Gondar", "Lalibela", "Babile", "Jimma", "Bale", "Sof Oumer", "Arba Minch"}
cost, path = multi_goal_ucs(graph, "Addis Ababa", goals)
print("Total cost:", cost)
print("Path:", " -> ".join(path))
