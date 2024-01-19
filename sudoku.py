import pygame as pg
import sys
import time

# مقداردهی اولیه Pygame
pg.init()
screen_size = 750, 750
screen = pg.display.set_mode(screen_size)
pg.display.set_caption("Sudoku")

# تابع بررسی صحت یک عدد در یک موقعیت خاص در جدول سودوکو
def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

# پیدا کردن یک مکان خالی در جدول سودوکو
def find_empty_location(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return i, j
    return None

# حل سودوکو با استفاده از الگوریتم بازگشتی
def solve_sudoku(board):
    empty_loc = find_empty_location(board)
    if not empty_loc:
        return True

    row, col = empty_loc
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            draw_background(board, row, col, highlight=True)
            pg.display.flip()
            pg.display.update()
            time.sleep(0.05)

            if solve_sudoku(board):
                return True

            board[row][col] = 0
            draw_background(board, row, col, highlight=False)
            pg.display.flip()
            pg.display.update()
            time.sleep(0.05)

    return False

# تابع رسم یک دایره در موقعیت خاص
def draw_box(y, x, dif):
    center = ((x + 0.7) * dif, (y + 0.7) * dif)
    radius = dif // 2 - 2
    pg.draw.circle(screen, pg.Color("green"), center, radius, 5)

# تابع رسم تخته سودوکو و اعداد آن
def draw_background(board, x, y, highlight=None):
    dif = 80
    screen.fill(pg.Color("white"))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(15, 15, 720, 720), 10)
    i = 1
    while (i * dif) < 720:
        line_width = 5 if i % 3 > 0 else 10
        pg.draw.line(
            screen,
            pg.Color("black"),
            pg.Vector2((i * dif) + 15, 15),
            pg.Vector2((i * dif) + 15, 730),
            line_width,
        )
        pg.draw.line(
            screen,
            pg.Color("black"),
            pg.Vector2(15, (i * dif) + 15),
            pg.Vector2(730, (i * dif) + 15),
            line_width,
        )
        i += 1

    font = pg.font.Font(None, 70)
    for i in range(9):
        for j in range(9):
            if board[i][j] != 0:
                text_color = pg.Color("black")
                if highlight and (i, j) == (x, y):
                    text_color = pg.Color("red")
                    draw_box(x, y, dif)
                text = font.render(str(board[i][j]), True, text_color)
                text_rect = text.get_rect(center=(55 + j * dif, 55 + i * dif))
                screen.blit(text, text_rect)

# تابع بررسی صحت ورودی سودوکو
def is_valid_input(board):
    for i in range(9):
        row_set = set()
        col_set = set()
        for j in range(9):
            if board[i][j] != 0 and board[i][j] in row_set:
                return False
            if board[j][i] != 0 and board[j][i] in col_set:
                return False
            row_set.add(board[i][j])
            col_set.add(board[j][i])
    return True

# جدول سودوکو ابتدایی
sudoku_board = [
    [1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 2, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 0, 0, 0, 0, 0, 0, 0],
]

# بررسی صحت ورودی سودوکو
if not is_valid_input(sudoku_board):
    print("Sudoku is wrong please fix it!")
    sys.exit()

# حل سودوکو
solve_sudoku(sudoku_board)

# نمایش تخته سودوکو
draw_background(sudoku_board, 0, 0)
pg.display.flip()
pg.display.update()

# حلقه اصلی Pygame برای نمایش بازی
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
