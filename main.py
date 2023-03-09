from pyautogui import KEYBOARD_KEYS
from Getch import _Getch
import solver, pynput, time, board_parser
from puzzlegraph import draw_puzzle

size_to_target = {5:1, 6:1, 8:1, 10:2, 14:3, 17:4, 21:5, 25:6}
mouse = pynput.mouse.Controller()
parser = board_parser.Parser()
getch = _Getch()

def check_type_y():
    while True:
        key = getch()
        if key == 'y':
            return True

        if key == 'n':
            return False

while True:
    print("Please make sure the grid is fully displayed on the screen and all cells are cleared.")
    if not parser.top_left or not parser.bottom_right:
        print("Move your mouse onto the top left cell of the grid and press 'p' ...")
        while getch() != 'p':
            continue
        parser.set_top_left()
        print("The top left corner is set.")

        print("Move your mouse onto the bottom right cell of the grid and press 'p' ...")
        while getch() != 'p':
            continue
        parser.set_bottom_right()
        print("The bottom right corner is set.")

    else:
        print("Keep using the previous corner or not? (Y/N)")
        if not check_type_y():
            parser.reset()
            continue

    try:
        print("Parsing puzzle...")
        blocks = parser.parse()
    except:
        print("Parse puzzle failed.")
        parser.reset()
        continue

    size = len(blocks)
    try:
        target = size_to_target[size]
    except:
        continue

    draw_puzzle(blocks)
    print('solving ...')

    s = solver.Solver(size, target, blocks)
    path = s.solve()

    x_step = (parser.bottom_right[0] - parser.top_left[0]) / (size - 1)
    y_step = (parser.bottom_right[1] - parser.top_left[1]) / (size - 1)

    mouse.position = (parser.top_left[0], parser.top_left[1])
    time.sleep(0.005)
    mouse.click(pynput.mouse.Button.left)

    for x, y in path:
        mouse.position = (parser.top_left[0] + y * x_step, parser.top_left[1] + x * y_step)
        time.sleep(0.005)
        mouse.click(pynput.mouse.Button.left)

    print("Continue? (Y/N)")
    if not check_type_y():
        break