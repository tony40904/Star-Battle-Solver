import pynput, pyautogui
import numpy as np

class Parser:

    scale = 1
    threshold = 0
    size = 0
    image = None
    block_label = []

    def __init__(self) -> None:
        self.mouse = pynput.mouse.Controller()
        self.top_left = None
        self.bottom_right = None

    def set_top_left(self):
        x, y = self.mouse.position
        self.top_left = (int(x), int(y))

    def set_bottom_right(self):
        x, y = self.mouse.position
        self.bottom_right = (int(x), int(y))

    def reset(self):
        self.top_left = None
        self.bottom_right = None

    def is_connect(self, p1, p2):
        image_shape = np.array(self.image.shape)
        p1 = np.array(p1)
        p2 = np.array(p2)
        step = (p2 - p1)
        start = np.abs(p1 * (image_shape // (self.size - 1)) - [1,1])
        end = np.abs(p2 * (image_shape // (self.size - 1)) - [1,1])
        count = 0
        while not np.array_equal(start, end):
            if self.image[start[0]][start[1]] < 128:
                count += 1
            elif count > 0:
                break
            start += step

        return count < self.threshold

    def find_size_and_thres(self):
        size = 1
        min_edge = 100
        max_edge = 0
        i = 0
        while i < self.image.shape[1]:
            if self.image[0][i] >= 128:
                i += 1
            else:
                size += 1
                count = 0
                while self.image[0][i] < 128:
                    i += 1
                    count += 1
                min_edge = min(min_edge, count)
                max_edge = max(max_edge, count)
        if min_edge * 3 > max_edge:
            self.threshold = min_edge * 3
        else:
            self.threshold = (min_edge + max_edge) // 2
        self.size = size

    def parse(self):
        length = (self.bottom_right[0] - self.top_left[0], self.bottom_right[1] - self.top_left[1])
        im = pyautogui.screenshot(region=(self.scale * self.top_left[0], self.scale * self.top_left[1], self.scale * length[0], self.scale * length[1])).convert('L')
        
        self.image = np.array(im)
        self.find_size_and_thres()
        self.block_label = [None] * self.size
        for i in range(self.size):
            self.block_label[i] = [None] * self.size
        id = 0
        stack = []
        dirs = [(0,1), (0,-1), (1,0), (-1,0)]
        for i in range(self.size):
            for j in range(self.size):
                if self.block_label[i][j] == None:
                    self.block_label[i][j] = id
                    stack.append((i, j))
                    
                    while stack:
                        x, y = stack.pop()
                        for mx, my in dirs:
                            next_x, next_y = x + mx, y + my
                            if next_x >= 0 and next_x < self.size and next_y >= 0 and next_y < self.size\
                                        and self.block_label[next_x][next_y] == None and self.is_connect((x, y), (next_x, next_y)):
                                self.block_label[next_x][next_y] = id
                                stack.append((next_x, next_y))
                    id += 1
        return self.block_label

