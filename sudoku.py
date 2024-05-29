import random


def print_board(board):
    """Wyświetla plansze sudoku"""

    top_line = "╔═══╤═══╤═══╦═══╤═══╤═══╦═══╤═══╤═══╗"
    middle_separator = "╟───┼───┼───╫───┼───┼───╫───┼───┼───╢"
    thick_separator = "╠═══╪═══╪═══╬═══╪═══╪═══╬═══╪═══╪═══╣"
    bottom_line = "╚═══╧═══╧═══╩═══╧═══╧═══╩═══╧═══╧═══╝"
    column_labels = "  a   b   c | d   e   f | g   h   i"

    print("\n" + top_line)
    for i in range(9):
        if i in [3, 6]:
            print(thick_separator)
        elif i != 0:
            print(middle_separator)
        row = "║"
        for j in range(9):
            if board[i][j] == 0:
                row += "   "
            else:
                row += f" {board[i][j]} "
            if j in [2, 5, 8]:
                row += "║"
            else:
                row += "│"
        row += f" {i + 1}"
        print(row)
    print(bottom_line)
    print(column_labels)

def col_letter_to_index(letter):
    """Zamiana litery kolumny na liczbę (0-8)"""
    return ord(letter.lower()) - ord('a')

def find_empty(board):
    """Znajdowanie pustych pól (zapisane w tablicy jako 0)"""
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)  # row, col
    return None


def valid(board, num, pos):
    """Sprawdzanie czy ruch jest prawidłowy"""
    # Sprawdzanie rzędu
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    # Sprawdzanie kolumny
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    # Sprawdzanie w kwadracie
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False

    return True


def solve(board):
    """Wypełnianie reszty pól"""
    find = find_empty(board)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0

    return False


def generate_board():
    """Generowanie planszy sudoku"""
    board = [[0 for _ in range(9)] for _ in range(9)]

    # Wypełnianie najpierw przękątnych kwadratów losowymi cyframi
    for i in range(0, 9, 3):
        fill_diagonal_box(board, i, i)
    # print_board(board) # Wyświetla wypełnione przekątne

    # Wypełnienie reszty tablicy
    solve(board)

    # Usuwanie losowych pól (ustawianie ich na 0)
    remove_elements(board)

    return board


def fill_diagonal_box(board, row, col):
    """Wypełnianie przekątnych"""
    nums = random.sample(range(1, 10), 9)
    for i in range(3):
        for j in range(3):
            board[row + i][col + j] = nums[i * 3 + j]


def remove_elements(board):
    """Usuwanie elementów tablicy"""
    print("Witaj w sudoku, wybierz poziom trudności: \n1. Łatwy\n2. Średni\n3. Trudny")
    difficulty = input()

    match difficulty:
        case "1": num_holes = 15
        case "2": num_holes = 25
        case "3": num_holes = 35
        case _: num_holes = 5
    count = num_holes
    while count > 0:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        while board[row][col] == 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
        board[row][col] = 0
        count -= 1




def main():
    """Pętla w main"""
    board = generate_board()
    print_board(board)

    while True:
        print("Wykonaj ruch w formacie 'kolumna rząd cyfra' (np. 'a 1 5') albo 'q' aby zakończyć:")
        move = input().strip()
        if move == 'q':
            break
        try:
            col_letter, row_str, num_str = move.split()
            row = int(row_str)
            num = int(num_str)
            col = col_letter_to_index(col_letter)
            if valid(board, num, (row - 1, col)):
                board[row - 1][col] = num
                print_board(board)
                if not find_empty(board):
                    print("Gratulacje! Wygrałeś!")
                    break
            else:
                print("Nieprawidłowy ruch. Spróbuj ponownie.")
        except (ValueError, IndexError):
            print("Nieprawidłowe wejście.")


if __name__ == "__main__":
    main()
