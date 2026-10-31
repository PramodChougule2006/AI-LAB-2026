
import random

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


def hill_climbing(n):
    for restart in range(5000):

        # Random initial board
        board = [random.randint(0, n - 1) for _ in range(n)]

        sideways = 0

        while True:
            current_h = heuristic(board, n)

            # Goal test
            if current_h == 0:
                return board

            best_h = current_h
            best_moves = []

            # Generate neighboring states
            for col in range(n):
                for row in range(n):

                    if row != board[col]:
                        new_board = board[:]
                        new_board[col] = row

                        h = heuristic(new_board, n)

                        if h < best_h:
                            best_h = h
                            best_moves = [new_board]

                        elif h == best_h:
                            best_moves.append(new_board)

            # No improvement possible
            if best_h > current_h or sideways >= 50:
                break

            if best_h == current_h:
                sideways += 1
            else:
                sideways = 0

            board = random.choice(best_moves)

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
    solution = hill_climbing(n)

    if solution is not None:
        print("\nSolution Found!")
        print("Heuristic value:", heuristic(solution, n))
        print("\nChessboard:")
        print_board(solution, n)
    else:
        print("Solution not found. Try again.")
