import solver, pynput, time, board_parser
from puzzlegraph import draw_puzzle

size_to_target = {5:1, 6:1, 8:1, 10:2, 14:3, 17:4, 21:5, 25:6}
mouse = pynput.mouse.Controller()
c, l = None, None

while True:
    try:
        p = board_parser.Parser(c, l)
        c, l = p.locate()
        if p.quit_sign:
            break
        block = p.parse()
        size = len(block)
        try:
            target = size_to_target[size]
        except:
            continue

        draw_puzzle(block)
        print('solving ...')

        s = solver.Solver(size, target, block)
        path = s.solve()

        x_step = l[0] / (size - 1)
        y_step = l[1] / (size - 1)

        for x, y in path:
            mouse.position = (c[0] + y * x_step, c[1] + x * y_step)
            time.sleep(0.005)
            mouse.click(pynput.mouse.Button.left)
    except:
        continue