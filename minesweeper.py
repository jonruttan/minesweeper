#!/usr/bin/env python

#Title:       Python3 Minesweeper  
#Description: A version of the Minesweeper game for the terminal written in Python3.  
#Keywords:    [#python, #minesweeper]  
#Author:      "[Jon Ruttan](jonruttan@gmail.com)"  
#Date:        2022-06-18  
#Revision:    1 (2022-06-18)  

import random

class Minesweeper:
    _mine = 9
    _marked = 10
    _hidden = 20
    #_chars = ' 12345678*' + 'X' * 10 + '.' * 10
    _chars = ' ❶❷❸❹❺❻❼❽✪' + '⚑' * 10 + '∙' * 10

    def __init__(self, width = 10, height = 10, mines = 10):
        self._width = width
        self._height = height
        self._mines = mines
        self.new()

    def new(self):
        self._board = [0] * self._width * self._height

        mines = self._mines
        while mines > 0:
            i = random.randrange(len(self._board))
            if self._board[i] != self._mine:
                self._board[i] = self._mine
                mines -= 1

    def inc(self, x, y):
        for y1 in range(max(0, y - 1), min(self._height, y + 2)):
            y2 = y1 * self._width
            for x1 in range(max(0, x - 1), min(self._width, x + 2)):
                i = y2 + x1
                if self._board[i] != self._mine:
                    self._board[i] += 1

    def counts(self):
        i = 0
        for y in range(0, self._height):
            for x in range(0, self._width):
                if self._board[i] == self._mine:
                    self.inc(x, y)
                i += 1

    def hide(self):
        for i in range(0, self._width * self._height):
            self._board[i] += self._hidden

    def reveal(self):
        for i in range(0, self._width * self._height):
            self._board[i] %= 10

    def click(self, x, y):
        l = {(x, y)}

        while len(l):
            (x, y) = l.pop()
            i = y * self._width + x

            if self._board[i] % 10 == self._mine:
                self.reveal()
                self.display()
                exit('You lose.')

            if self._board[i] >= self._hidden:
                self._board[i] -= self._hidden

            if self._board[i] != 0:
                return

            for y1 in range(max(0, y - 1), min(self._height, y + 2)):
                y2 = y1 * self._width
                for x1 in range(max(0, x - 1), min(self._width, x + 2)):
                    i = y2 + x1
                    if self._board[i] >= self._hidden:
                        self._board[i] -= self._hidden
                        if self._board[i] == 0:
                            l.add((x1, y1))

    def mark(self, x, y):
        i = y * self._width + x

        if self._board[i] >= self._hidden:
            self._board[i] -= self._marked
        elif self._board[i] >= self._marked:
            self._board[i] += self._marked

    def win(self):
        for i in range(0, self._width * self._height):
            if self._board[i] >= self._hidden:
                return False

        return True

    def display(self):
        print('  ', end='')
        for x in range(0, self._width):
            print(f'{x} ', end='')

        print()

        i = 0
        for y in range(0, self._height):
            print(f'{y} ', end='')
            for x in range(0, self._width):
                n = self._board[i]
                c = self._chars[n]
                print(f'{c} ', end='')
                i += 1
            print()


if __name__ == "__main__":
    import sys

    opts = (opt for opt in sys.argv[1:] if opt.startswith("-"))
    args = (arg for arg in sys.argv[1:] if not arg.startswith("-"))

    for opt in opts:
        if opt == '-h':
            raise SystemExit(f"Usage: {sys.argv[0]} (-h) <width> <height> <mines>")
        elif opt == '-d':
            print('Debug mode')
            random.seed(1)

    (width, height, mines) = (tuple(int(i) for i in args) + (10, 10, 10))[:3]

    minesweeper = Minesweeper(width, height, mines)
    minesweeper.counts()
    minesweeper.hide()

    while True:
        minesweeper.display()

        if minesweeper.win():
            exit('You win!')

        move = input('Enter move: ') + ' 0'
        (x, y, m) = (int(i) for i in move.split(' ')[:3])

        if m > 0:
            minesweeper.mark(x, y)
        else:
            minesweeper.click(x, y)
