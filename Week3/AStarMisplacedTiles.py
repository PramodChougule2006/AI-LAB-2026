import heapq

class PuzzleState:
    def __init__(self, board, g=0, parent=None):
        self.board = board       # Tuple of tuples (e.g., ((1, 2, 3), (4, 0, 5), (6, 7, 8)))
        self.g = g               # Cost from start to current node
        self.parent = parent     # Parent node to reconstruct path
        self.h = self.calculate_misplaced_tiles()
        self.f = self.g + self.h

    def calculate_misplaced_tiles(self):
        # Flattened standard goal state for an 8-puzzle: 1, 2, 3, 4, 5, 6, 7, 8, 0
        goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)
        flat_board = [tile for row in self.board for tile in row]
        
        misplaced = 0
        for i in range(len(flat_board)):
            # Ignore the blank tile (0) when counting misplaced tiles
            if flat_board[i] != 0 and flat_board[i] != goal[i]:
                misplaced += 1
        return misplaced

    # Tie-breaking for the priority queue
    def __lt__(self, other):
        return self.f < other.f

def get_neighbors(state):
    neighbors = []
    board = [list(row) for row in state.board]
    
    # Find coordinates of the blank space (0)
    r, c = 0, 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
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

    while open_set:
        current = heapq.heappop(open_set)
        
        if current.board == goal_board:
            # Reconstruct path
            path = []
            while current:
                path.append(current.board)
                current = current.parent
            return path[::-1] # Return path from start to goal
            
        if current.board in closed_set and closed_set[current.board] <= current.g:
            continue
            
        closed_set[current.board] = current.g
        
        for neighbor in get_neighbors(current):
            if neighbor.board in closed_set and closed_set[neighbor.board] <= neighbor.g:
                continue
            heapq.heappush(open_set, neighbor)
            
    return None # No solution found

# --- Example Usage ---
# 0 represents the empty slot
start = (
    (1, 2, 3),
    (0, 4, 6),
    (7, 5, 8)
)

solution_path = solve_a_star(start)

if solution_path:
    print(f"Solved in {len(solution_path) - 1} steps:")
    for step, board in enumerate(solution_path):
        print(f"\nStep {step}:")
        for row in board:
            print(row)
else:
    print("No solution found.")
