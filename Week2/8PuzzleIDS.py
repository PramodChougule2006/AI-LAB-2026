class PuzzleState:
    def __init__(self, board, parent=None, move=None):
        self.board = board        # 1D array of 9 elements representing the 3x3 board
        self.parent = parent      # Link to the parent state to reconstruct the path
        self.move = move          # The action taken to reach this state ('Up', 'Down', etc.)

    def get_blank_index(self):
        return self.board.index(0)

    def get_neighbors(self):
        neighbors = []
        zero_idx = self.get_blank_index()
        row, col = divmod(zero_idx, 3)

        # Define possible moves for the blank tile (0)
        moves = [
            (-1, 0, 'Up'),
            (1, 0, 'Down'),
            (0, -1, 'Left'),
            (0, 1, 'Right')
        ]

        for dr, dc, move_name in moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_idx = new_row * 3 + new_col
                
                # Create a copy of the current board layout
                new_board = list(self.board)
                # Swap the blank space with the target tile
                new_board[zero_idx], new_board[new_idx] = new_board[new_idx], new_board[zero_idx]
                
                neighbors.append(PuzzleState(new_board, self, move_name))
        
        return neighbors

def depth_limited_dfs(current_state, goal_state, depth_limit, visited):
    # Check if the goal state is reached
    if current_state.board == goal_state:
        return current_state
        
    # If the limit is reached, stop exploring this branch
    if depth_limit <= 0:
        return None

    # Add current board state to visited to prevent loops in this branch path
    current_tuple = tuple(current_state.board)
    visited.add(current_tuple)

    # Explore neighbors
    for neighbor in current_state.get_neighbors():
        if tuple(neighbor.board) not in visited:
            # Recursive call with decremented depth limit
            result = depth_limited_dfs(neighbor, goal_state, depth_limit - 1, visited)
            if result is not None:
                return result
                
    # Backtrack: Remove from visited so it can be explored via other paths if needed
    visited.remove(current_tuple)
    return None

def solve_ids(start_state, goal_state, max_depth):
    # Progressively increase the maximum allowed depth limit up to user specification
    for depth in range(max_depth + 1):
        # Visited set tracks ancestors on the current DFS path to avoid infinite loops
        visited = set()
        initial_state = PuzzleState(start_state)
        
        result = depth_limited_dfs(initial_state, goal_state, depth, visited)
        if result is not None:
            return result
            
    return None

def print_solution(solution_state):
    path = []
    current = solution_state
    
    # Trace backwards from goal to start
    while current:
        path.append(current)
        current = current.parent
    path.reverse()

    print(f"\nGoal reached optimally in {len(path) - 1} moves!\n")
    for step, state in enumerate(path):
        if state.move:
            print(f"Step {step}: Move blank {state.move}")
        else:
            print("Initial Configuration:")
            
        # Display the 3x3 layout
        for i in range(0, 9, 3):
            print(state.board[i:i+3])
        print("-" * 15)

def get_user_input():
    print("Enter the initial state of the 8-puzzle.")
    print("Use numbers 1-8 for the tiles, and 0 for the empty/blank space.")
    print("Example format (separated by spaces): 1 2 3 4 0 6 7 5 8")
    
    while True:
        try:
            user_str = input("\nEnter your initial state: ")
            board = [int(x) for x in user_str.split()]
            
            # Validation checks
            if len(board) != 9:
                print("Error: You must enter exactly 9 numbers.")
                continue
                
            if sorted(board) != list(range(9)):
                print("Error: Input must contain numbers from 0 to 8 without duplicates.")
                continue
                
            return board
        except ValueError:
            print("Error: Please enter numbers only separated by spaces.")

def get_depth_limit():
    while True:
        try:
            limit = int(input("Enter the maximum depth limit for Iterative Deepening (e.g., 20): "))
            if limit < 0:
                print("Error: Depth limit must be a positive integer.")
                continue
            return limit
        except ValueError:
            print("Error: Please enter a valid integer number.")

# --- Execution ---
if __name__ == "__main__":
    # Get the starting arrangement from the user
    initial_configuration = get_user_input()
    
    # Get the search limit constraint from the user
    user_max_depth = get_depth_limit()

    # Standard targeted goal state
    goal_configuration = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    print(f"\nSearching for the optimal solution using IDS (Limit: {user_max_depth})...")
    result = solve_ids(initial_configuration, goal_configuration, user_max_depth)

    if result:
        print_solution(result)
    else:
        print(f"No solution could be found within the user-specified limit of {user_max_depth} depth levels.")
