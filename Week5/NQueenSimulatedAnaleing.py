
import random
import math

def heuristic(board, n):
    conflicts = 0

    for i in range(n):
        for j in range(i + 1, n):

            # Same row conflict
            if board[i] == board[j]:
                conflicts += 1

            # Diagonal conflict
            elif abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1

    return conflicts


def simulated_annealing(n):
    # Random initial state
    board = [random.randint(0, n - 1) for _ in range(n)]

    temperature = 1000
    cooling_rate = 0.995
    min_temperature = 0.0001

    while temperature > min_temperature:

        current_h = heuristic(board, n)

        # Goal test
        if current_h == 0:
            return board

        # Generate a neighboring state
        new_board = board[:]

        col = random.randint(0, n - 1)
        row = random.randint(0, n - 1)

        new_board[col] = row

        new_h = heuristic(new_board, n)

        # Calculate change in heuristic
        delta = current_h - new_h

        # Accept better moves
        if delta > 0:
            board = new_board

        # Accept worse moves with probability
        elif random.random() < math.exp(delta / temperature):
            board = new_board

        # Reduce temperature
        temperature *= cooling_rate

    # Final goal check
    if heuristic(board, n) == 0:
        return board

    return None


def print_board(board, n):
    for row in range(n):
        for col in range(n):
            if board[col] == row:
                print("Q", end=" ")
            else:
                print(".", end=" ")
        print()


# Main program
n = int(input("Enter number of queens: "))

if n == 2 or n == 3:
    print("No solution exists.")
else:
    solution = None

    # Random restart
    for attempt in range(1000):
        solution = simulated_annealing(n)

        if solution is not None:
            break

    if solution is not None:
        print("\nSolution Found!")
        print("Heuristic value:", heuristic(solution, n))
        print("\nChessboard:")
        print_board(solution, n)
    else:
        print("\nSolution not found. Try again.")
