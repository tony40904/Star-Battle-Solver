class Solver:

    stack = []
    walked = set()
    try_count = 0

    def __init__(self, size, target, block_map) -> None:
        self.size = size
        self.target = target
        self.board = [None] * size
        self.block_of_grid = [None] * size
        self.block_grids = [None] * size
        self.blocks = []
        for i in range(size):
            self.board[i] = [False] * size
            self.block_of_grid[i] = [None] * size
            self.block_grids[i] = []
            self.blocks.append(self.Block(i))
        self.rows = [0] * size
        self.cols = [0] * size
        self.init_blocks(block_map)

        next_steps = self.explore()
        for step in next_steps:
            path = [step]
            self.walked.add(tuple(path))
            self.stack.append(([step], self.copy_board(), self.rows.copy(), self.cols.copy(), self.copy_blocks()))
        

    def init_blocks(self, block_map):
        for x in range(self.size):
            for y in range(self.size):
                block_id = block_map[x][y]
                self.block_of_grid[x][y] = self.blocks[block_id]
                self.blocks[block_id].valid += 1
                self.block_grids[block_id].append((x, y))

    def put(self, x, y):
        self.board[x][y] = 'star'
        for i in range(x-1, x+2):
            for j in range(y-1, y+2):
                if i >= 0 and j >= 0 and i < self.size and j < self.size and self.board[i][j] == False:
                    self.board[i][j] = True
                    self.block_of_grid[i][j].valid -= 1

        self.rows[x] += 1
        if self.rows[x] == self.target:
            for j in range(self.size):
                if self.board[x][j] == False:
                    self.board[x][j] = True
                    self.block_of_grid[x][j].valid -= 1

        self.cols[y] += 1
        if self.cols[y] == self.target:
            for i in range(self.size):
                if self.board[i][y] == False:
                    self.board[i][y] = True
                    self.block_of_grid[i][y].valid -= 1
        block = self.block_of_grid[x][y]
        block.put()
        if block.count == self.target:
            for i, j in self.block_grids[block.id]:
                if self.board[i][j] == False:
                    self.board[i][j] = True
                    self.block_of_grid[i][j].valid -= 1

    def check(self):
        for k in range(self.size):
            row_valid = 0
            col_valid = 0
            for m in range(self.size):
                if self.board[k][m] == False:
                    row_valid += 1
                if self.board[m][k] == False:
                    col_valid += 1
            if self.target - self.rows[k] > row_valid or self.target - self.cols[k] > col_valid:
                return False

        for block in self.blocks:
            if self.target - block.count > block.valid:
                return False

        return True

    def explore(self):
        min_block_id = None
        for block in self.blocks:
            if block.valid > 0:
                if min_block_id == None:
                    min_block_id = block.id
                else:
                    if block.valid < self.blocks[min_block_id].valid:
                        min_block_id = block.id

        res = []
        for x, y in self.block_grids[min_block_id]:
            if self.board[x][y] == False:
                res.append((x, y))

        return res

    def display(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] == 'star':
                    print('★', end = ' ')
                elif self.board[x][y] == True:
                    print('-', end = ' ')
                else:
                    print(' ', end = ' ')
            print('')

    def copy_board(self):
        board = [None] * self.size
        for i in range(self.size):
            board[i] = self.board[i].copy()
        return board

    def copy_blocks(self):
        blocks = [None] * self.size
        for i in range(self.size):
            blocks[i] = self.blocks[i].copy()
        return blocks

    def solve(self):
        path = []
        while self.stack:
            self.try_count += 1
            path, self.board, self.rows, self.cols, self.blocks = self.stack.pop()

            for block in self.blocks:
                for x, y in self.block_grids[block.id]:
                    self.block_of_grid[x][y] = block

            self.put(path[-1][0], path[-1][1])
            
            if len(path) == self.size * self.target:
                break

            if self.check():
                next_steps = self.explore()
                for next_step in next_steps:
                    next_path = path + [next_step]
                    _next_path = next_path.copy()
                    _next_path.sort()
                    _next_path = tuple(_next_path)
                    if _next_path not in self.walked:
                        self.walked.add(_next_path)
                        self.stack.append((next_path, self.copy_board(), self.rows.copy(), self.cols.copy(), self.copy_blocks()))

        self.display()
        print('try: ', self.try_count)
        print('walked: ', len(self.walked))
        print("=" * (2 * self.size + 1))
        return path
    
    class Block:
        def __init__(self, i) -> None:
            self.count = 0
            self.valid = 0
            self.id = i
        
        def copy(self):
            new_block = self.__class__(self.id)
            new_block.count = self.count
            new_block.valid = self.valid
            return new_block

        def put(self):
            self.count += 1
            self.valid -= 1

        def __str__(self) -> str:
            return str('c: ' + self.count + ', v: ' + self.valid)
        
        def __repr__(self) -> str:
            return '(id:' + str(self.id) + ',c:' + str(self.count) + ',v:' + str(self.valid) + ')'
