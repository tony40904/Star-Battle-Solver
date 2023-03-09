box = {0:'  ', 3:'┗━', 5:'┃ ', 9:'┛ ', 6:'┏━', 10:'━━', 12: '┓ ', 
        11:'┻━', 7:'┣━', 14:'┳━', 13:'┫ ', 15:'╋━'}

dirs = [(0,0), (0,1), (1,1), (1,0), (0,0)]

def draw_puzzle(b):
    block = []
    for row in b:
        block.append(row.copy())

    for i in range(len(b)):
        block[i].insert(0, -1)
        block[i].append(-1)
    block.insert(0, [-1] * (len(b) + 2))
    block.append([-1] * (len(b) + 2))

    for i in range(len(block) - 1):
        for j in range(len(block[0]) - 1):
            draw(block, i, j)
        print('')

def draw(block, x, y):
    num = 0
    for i in range(4):
        t1 = block[x + dirs[i][0]][y + dirs[i][1]]
        t2 = block[x + dirs[i + 1][0]][y + dirs[i + 1][1]]
        if not t1 == t2:
            num += 2 ** i
    print(box[num], end='')