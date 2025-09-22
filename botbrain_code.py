import math
from queue import PriorityQueue

# Campus graph: adjacency list with distances (weights)
campus_graph = {
    "Sports Area": [("Hostel Block-1", 200)],
    "Hostel Block-1": [("Sports Area", 200), ("Food Court", 150)],
    "Food Court": [("Hostel Block-1", 150), ("Academic Block 2 (B)", 150)],
    "Academic Block 2 (B)": [("Food Court", 150), ("Library", 100)],
    "Library": [("Academic Block 2 (B)", 100), ("Admin Block", 20), ("Academic Block 1 (A)", 20)],
    "Admin Block": [("Library", 20), ("Academic Block 1 (A)", 20)],
    "Academic Block 1 (A)": [("Admin Block", 20), ("Library", 20), ("Canteen", 25)],
    "Canteen": [("Academic Block 1 (A)", 25), ("Medical Centre", 25)],
    "Medical Centre": [("Canteen", 25), ("Auditorium", 25)],
    "Auditorium": [("Medical Centre", 25), ("Second Gate", 75)],
    "Second Gate": [("Auditorium", 75), ("Main Gate", 100)],
    "Main Gate": [("Second Gate", 100)],
}

# Building Timings
building_timings = {
    "Library": "8:30 AM – 9:00 PM",
    "Canteen": "8:00 AM – 4:45 PM",
    "Medical Centre": "24/7",
    "Sports Area": "6:00 AM – 7:30 PM",
    "Admin Block": "9:00 AM – 5:00 PM",
    "Auditorium": "10:00 AM – 5:00 PM",
}

# Approximate coordinates for heuristic calculation (Euclidean distance)
campus_coordinates = {
    "Sports Area": (0, 150),
    "Hostel Block-1": (0, 0),
    "Food Court": (50, 0),
    "Academic Block 2 (B)": (150, 0),
    "Library": (225, 0),
    "Admin Block": (250, 25),
    "Academic Block 1 (A)": (275, 0),
    "Canteen": (300, 0),
    "Medical Centre": (325, -25),
    "Auditorium": (350, -50),
    "Second Gate": (350, -70),
    "Main Gate": (350, -120),
}

# Heuristic function: Euclidean distance
def euclidean_heuristic(node1, node2):
    x1, y1 = campus_coordinates[node1]
    x2, y2 = campus_coordinates[node2]
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# A* Search (default algorithm)
def a_star(start, goal):
    visited = set()
    pq = PriorityQueue()
    pq.put((euclidean_heuristic(start, goal), 0, start, [start]))
    explored_nodes = []

    while not pq.empty():
        f_score, cost, current, path = pq.get()
        explored_nodes.append(current)
        if current == goal:
            return path, cost, explored_nodes
        if current not in visited:
            visited.add(current)
            for neighbor, weight in campus_graph.get(current, []):
                if neighbor not in visited:
                    g = cost + weight
                    h = euclidean_heuristic(neighbor, goal)
                    pq.put((g + h, g, neighbor, path + [neighbor]))
    return None, math.inf, explored_nodes

# Display result
def display_result(start, goal):
    path, dist, explored = a_star(start, goal)
    if path is None:
        return f"No path found from {start} to {goal}."

    # Walking speed approx 5 km/h = 1.25 m/s
    walking_time = dist / 1.25
    walking_minutes = walking_time / 60

    result = f"\nDirections from {start} to {goal}:\n"
    result += " -> ".join(path) + "\n"
    result += f"Total distance: {dist} meters\n"
    result += f"Estimated walking time: {walking_minutes:.2f} minutes\n"

    # Add timings if available
    if goal in building_timings:
        result += f"{goal} Timings: {building_timings[goal]}\n"

    result += f"Nodes explored: {explored}\n"
    return result

# Show numbered locations
def show_locations():
    print("\nAvailable Locations:")
    for i, location in enumerate(campus_graph.keys(), 1):
        print(f"{i}. {location}")
    return list(campus_graph.keys())

def main():
    print("Welcome to BotBrain - Chanakya University Campus Navigator")

    while True:
        locations = show_locations()

        try:
            start_index = int(input("\nEnter start location number (or 0 to quit): "))
            if start_index == 0:
                break
            goal_index = int(input("Enter destination location number: "))

            if 1 <= start_index <= len(locations) and 1 <= goal_index <= len(locations):
                start = locations[start_index - 1]
                goal = locations[goal_index - 1]
                print(display_result(start, goal))
            else:
                print("Invalid numbers. Try again.")
        except ValueError:
            print("Please enter valid numbers only.")

        print("-" * 50)

if __name__ == "__main__":
    main()


