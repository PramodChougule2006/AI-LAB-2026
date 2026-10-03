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

def solve_dfs(start_state, goal_state):
    stack = [PuzzleState(start_state)]
    visited = {tuple(start_state)}

    while stack:
        current_state = stack.pop()

        if current_state.board == goal_state:
            return current_state

        for neighbor in current_state.get_neighbors():
            neighbor_tuple = tuple(neighbor.board)
            if neighbor_tuple not in visited:
                visited.add(neighbor_tuple)
                stack.append(neighbor)
                
    return None

def print_solution(solution_state):
    path = []
    current = solution_state
    
    while current:
        path.append(current)
        current = current.parent
    path.reverse()

    print(f"\nGoal reached in {len(path) - 1} moves!\n")
    for step, state in enumerate(path):
        if state.move:
            print(f"Step {step}: Move blank {state.move}")
        else:
            print("Initial Configuration:")
            
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
            # Split string by spaces and convert to integers
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

# --- Execution ---
if __name__ == "__main__":
    # Get the starting arrangement from the user
    initial_configuration = get_user_input()

    # Standard targeted goal state
    goal_configuration = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    print("\nSearching for a solution using DFS...")
    result = solve_dfs(initial_configuration, goal_configuration)

    if result:
        print_solution(result)
    else:
        print("No solution could be found.")
