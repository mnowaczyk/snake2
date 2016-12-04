#!/usr/bin/env python3

import curses
import random
import time

class CrashError(Exception):
    pass


class Food:
    def __init__(self, window):
        self.window = window
        self.blocks = []
        self.addFood()
    def draw(self):
        for block in self.blocks:
            window.move(block[1], block[0])
            window.addstr('█', curses.color_pair(3))

    def addFood(self):
        (h, w) = self.window.getmaxyx()
        x = int(random.random() * w)
        y = int(random.random() * h)
        self.blocks.append([x,y])
        

class Snake:
    DIR_UP=1
    DIR_RIGHT=2
    DIR_DOWN=3
    DIR_LEFT=4
    
    def __init__(self, window, food):
        self.window = window
        self.food = food
        self.eaten = 0
        (h, w) = self.window.getmaxyx()
        x = int(w/2)
        y = int(h/2)
        self.blocks = [[x, y], [x-1, y], [x-2, y], [x-3, y], [x-4, y]]
        self.direction = self.DIR_RIGHT
    
    def draw(self):
        for block in self.blocks:
            window.move(block[1], block[0])
            window.addstr('█', curses.color_pair(2))
        
    def move(self):
        head = self.blocks[0]
        if self.direction == self.DIR_UP:
            newHead = [head[0], head[1]-1]
        elif self.direction == self.DIR_DOWN:
            newHead = [head[0], head[1]+1]
        elif self.direction == self.DIR_RIGHT:
            newHead = [head[0]+1, head[1]]
        else:
            newHead = [head[0]-1, head[1]]
        (h, w) = self.window.getmaxyx()
        x = newHead[0]
        y = newHead[1]
        if x<0 or x>w-1 or y<0 or y>h-1:
            raise CrashError()
        if self.eaten <= 0:
            self.blocks.pop()
        else:
            self.eaten-=1
        if newHead in self.blocks:
            self.blocks.insert(0, newHead)
            raise CrashError()
        if newHead in self.food.blocks:
            self.food.blocks.remove(newHead)
            self.eaten+=5
            self.food.addFood()
        self.blocks.insert(0, newHead)
    
    def setDirection(self, direction):
        if abs(self.direction - direction) in [1, 3]:
            self.direction = direction
        

window = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.noecho()
curses.curs_set(False)
window.keypad(1)
window.nodelay(1)


try:
    
    k=curses.KEY_RIGHT
    food = Food(window)
    snake = Snake(window, food)
    (h, w) = window.getmaxyx()
    if w < 50 or h < 10:
        quit
    x = int(w/2)
    y = int(h/2)
    while True:
        window.clear()
        try:
            snake.move()
            snake.draw()
            food.draw()
        except CrashError:
            window.clear()
            window.move(y, x-8)
            window.addstr("GAME OVER! LENGTH: %d"%len(snake.blocks))
            window.refresh()
            time.sleep(5)
            break
        window.move(0,0)
        window.refresh()
    
        c = window.getch()
        if c !=curses.ERR:
            k = c
    
        if k == curses.KEY_LEFT:
            snake.setDirection(Snake.DIR_LEFT)
        elif k == curses.KEY_RIGHT:
            snake.setDirection(Snake.DIR_RIGHT)
        elif k == curses.KEY_UP:
            snake.setDirection(Snake.DIR_UP)
        elif k == curses.KEY_DOWN:
            snake.setDirection(Snake.DIR_DOWN)
        
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
finally:
    curses.endwin()
