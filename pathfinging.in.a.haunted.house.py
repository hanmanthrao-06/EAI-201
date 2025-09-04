import heapq

# New example grid
grid = [
    ['S', '0', '1', '0', '0'],
    ['0', '1', '0', '1', '0'],
    ['0', '0', '0', '1', '0'],
    ['1', '1', '0', '1', '0'],
    ['0', '0', '0', '0', 'G']
]

ROWS, COLS = len(grid), len(grid[0])
directions = [(-1,0), (1,0), (0,-1), (0,1)]  # up, down, left, right

# Find start and goal
def find_positions(grid):
    start = goal = None
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'G':
                goal = (r, c)
    return start, goal

# Manhattan distance heuristic
def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# Greedy Best-First Search
def greedy_bfs(start, goal):
    open_set = []
    heapq.heappush(open_set, (manhattan(start, goal), start))
    came_from = {start: None}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            break

        if current in visited:
            continue
        visited.add(current)

        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] != '1':
                neighbor = (nr, nc)
                if neighbor not in came_from:
                    came_from[neighbor] = current
                    heapq.heappush(open_set, (manhattan(neighbor, goal), neighbor))

    return reconstruct_path(came_from, start, goal)

# A* Search
def a_star(start, goal):
    open_set = []
    heapq.heappush(open_set, (manhattan(start, goal), 0, start))
    came_from = {start: None}
    g_score = {start: 0}

    while open_set:
        _, cost, current = heapq.heappop(open_set)

        if current == goal:
            break

        for dr, dc in directions:
            nr, nc = current[0] + dr, current[1] + dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc] != '1':
                neighbor = (nr, nc)
                new_cost = cost + 1
                if neighbor not in g_score or new_cost < g_score[neighbor]:
                    g_score[neighbor] = new_cost
                    priority = new_cost + manhattan(neighbor, goal)
                    heapq.heappush(open_set, (priority, new_cost, neighbor))
                    came_from[neighbor] = current

    return reconstruct_path(came_from, start, goal)

# Reconstruct path
def reconstruct_path(came_from, start, goal):
    if goal not in came_from:
        return None  # no path
    path = []
    node = goal
    while node:
        path.append(node)
        node = came_from[node]
    path.reverse()
    return path

# Run both searches
start, goal = find_positions(grid)

print("Greedy BFS Path:", greedy_bfs(start, goal))
print("A* Path:", a_star(start, goal))
