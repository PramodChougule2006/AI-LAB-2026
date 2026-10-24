import heapq

class PuzzleState:
    def __init__(self, board, g=0, parent=None):
        self.board = board       # Tuple of tuples (e.g., ((1, 2, 3), (4, 0, 5), (6, 7, 8)))
        self.g = g               # Cost from start to current node
        self.parent = parent     # Parent node to reconstruct path
        self.h = self.calculate_manhattan_distance()
        self.f = self.g + self.h

    def calculate_manhattan_distance(self):
        # Coordinates of where each tile (1-8) should ideally be in a standard goal state
        # Format: tile_value -> (row, col)
        goal_positions = {
            1: (0, 0), 2: (0, 1), 3: (0, 2),
            4: (1, 0), 5: (1, 1), 6: (1, 2),
            7: (2, 0), 8: (2, 1)
            # 0 (blank space) is intentionally omitted from the heuristic calculation
        }
        
        distance = 0
        for r in range(3):
            for c in range(3):
                tile = self.board[r][c]
                if tile != 0: # Ignore the blank tile
                    goal_r, goal_c = goal_positions[tile]
                    distance += abs(r - goal_r) + abs(c - goal_c)
        return distance

    # Tie-breaking for the priority queue
    def __lt__(self, other):
        return self.f < other.f

def get_neighbors(state):
    neighbors = []
    
    # Find coordinates of the blank space (0)
    r, c = 0, 0
    for i in range(3):
        for j in range(3):
            if state.board[i][j] == 0:
                r, c = i, j
                break

    # Possible moves: Up, Down, Left, Right
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            # Swap blank space with the neighbor tile
            new_board = [list(row) for row in state.board]
            new_board[r][c], new_board[nr][nc] = new_board[nr][nc], new_board[r][c]
            
            # Convert back to immutable tuple of tuples
            tuple_board = tuple(tuple(row) for row in new_board)
            neighbors.append(PuzzleState(tuple_board, state.g + 1, state))
            
    return neighbors

def solve_a_star(start_board):
    goal_board = ((1, 2, 3), (4, 5, 6), (7, 8, 0))
    start_state = PuzzleState(start_board)
    
    open_set = []
    heapq.heappush(open_set, start_state)
    
    # Store visited configurations and their lowest g-score
    closed_set = {} 
    nodes_expanded = 0

    while open_set:
        current = heapq.heappop(open_set)
        nodes_expanded += 1
        
        if current.board == goal_board:
            path = []
            while current:
                path.append(current.board)
                current = current.parent
            return path[::-1], nodes_expanded
            
        if current.board in closed_set and closed_set[current.board] <= current.g:
            continue
            
        closed_set[current.board] = current.g
        
        for neighbor in get_neighbors(current):
            if neighbor.board in closed_set and closed_set[neighbor.board] <= neighbor.g:
                continue
            heapq.heappush(open_set, neighbor)
            
    return None, nodes_expanded # No solution found

# --- Example Usage ---
# 0 represents the empty slot
start = (
    (1, 2, 3),
    (0, 4, 6),
    (7, 5, 8)
)

solution_path, total_nodes = solve_a_star(start)

if solution_path:
    print(f"Solved in {len(solution_path) - 1} steps.")
    print(f"Total nodes evaluated: {total_nodes}")
    for step, board in enumerate(solution_path):
        print(f"\nStep {step}:")
        for row in board:
            print(row)
else:
    print("No solution found.")
