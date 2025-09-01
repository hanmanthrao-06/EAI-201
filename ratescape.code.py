import heapq
import math


def euclidean_distance(a, b):
    """Calculate straight-line distance between two points a and b"""
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

# DFS Algorithm 
def dfs(graph, start, goal):
    stack = [(start, [start], 0)]
    visited = set()
    
    while stack:
        node, path, cost = stack.pop()
        if node == goal:
            return path, cost, len(visited)
        if node not in visited:
            visited.add(node)
            for neighbor, edge_cost in graph[node]:
                stack.append((neighbor, path + [neighbor], cost + edge_cost))
    return None, float('inf'), len(visited)

# BFS Algorithm 
def bfs(graph, start, goal):
    from collections import deque
    queue = deque([(start, [start], 0)])
    visited = set()
    
    while queue:
        node, path, cost = queue.popleft()
        if node == goal:
            return path, cost, len(visited)
        if node not in visited:
            visited.add(node)
            for neighbor, edge_cost in graph[node]:
                queue.append((neighbor, path + [neighbor], cost + edge_cost))
    return None, float('inf'), len(visited)

# Dijkstra Algorithm 
def dijkstra(graph, start, goal):
    pq = [(0, start, [start])]
    visited = set()
    
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node == goal:
            return path, cost, len(visited)
        if node not in visited:
            visited.add(node)
            for neighbor, edge_cost in graph[node]:
                if neighbor not in visited:
                    heapq.heappush(pq, (cost + edge_cost, neighbor, path + [neighbor]))
    return None, float('inf'), len(visited)

#  A* Algorithm 
def a_star(graph, coords, start, goal):
    pq = [(euclidean_distance(coords[start], coords[goal]), 0, start, [start])]
    visited = set()
    
    while pq:
        est_total, cost, node, path = heapq.heappop(pq)
        if node == goal:
            return path, cost, len(visited)
        if node not in visited:
            visited.add(node)
            for neighbor, edge_cost in graph[node]:
                if neighbor not in visited:
                    g = cost + edge_cost
                    h = euclidean_distance(coords[neighbor], coords[goal])
                    heapq.heappush(pq, (g + h, g, neighbor, path + [neighbor]))
    return None, float('inf'), len(visited)

if __name__ == "__main__":

    n, m = 6, 7
    coords = {
        0: (0, 0),
        1: (2, 2),
        2: (4, 2),
        3: (6, 0),
        4: (3, -2),
        5: (5, -2)
    }
    
    graph = {i: [] for i in range(n)}
    edges = [
        (0, 1, 3), (1, 2, 2), (2, 3, 4),
        (1, 4, 4), (4, 5, 3), (5, 3, 2),
        (2, 5, 2)
    ]
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))  
    start, goal = 0, 3  

    print("\n DFS")
    path, cost, visited = dfs(graph, start, goal)
    print(f"Path: {path}, Cost: {cost}, Visited: {visited}")

    print("\n BFS ")
    path, cost, visited = bfs(graph, start, goal)
    print(f"Path: {path}, Cost: {cost}, Visited: {visited}")

    print("\n Dijkstra ")
    path, cost, visited = dijkstra(graph, start, goal)
    print(f"Path: {path}, Cost: {cost}, Visited: {visited}")

    print("\n A* Search ")
    path, cost, visited = a_star(graph, coords, start, goal)
    print(f"Path: {path}, Cost: {cost}, Visited: {visited}")
