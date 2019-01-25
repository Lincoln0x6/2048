#coding=utf-8
import copy
import random
import operator
from tkinter import *
from tkinter import messagebox
import sys
from PIL import Image, ImageTk

class Game2048():

    def __init__(self):
        self.window = Tk()
        self.PASS_CONDITION = 2048
        self.GRID_NUMBER = 4
        self.score = 0
        self.IMAGE_SIZE = int(400/self.GRID_NUMBER)
        self.number2Pic = {}
        self.NUMBER_LIST = [0,2,4,8,16,32,64,128,256,512,1024,2048,4096,8192,16384,32768,65536,131072]
        self.loadImage()
        self.window.resizable(0, 0)
        self.window.geometry('420x420')
        self.window.title('2048游戏       score: ' + str(self.score))
        self.initMap()


    def initMap(self):
        self.window.bind("<Key>", self.main)
        self.window.focus_set()
        self.map = [[0 for i in range(self.GRID_NUMBER)] for j in range(self.GRID_NUMBER)]
        self.getNewNumber(2)
        self.updateMap()

    def updateMap(self):
        self.window.title('2048游戏       score: ' + str(self.score))
        for i in range(self.GRID_NUMBER):
            for j in range(self.GRID_NUMBER):
                Label(self.window, image=self.number2Pic[self.map[i][j]]).grid(row=i, column=j, sticky=W)

    def loadImage(self):
        for number in self.NUMBER_LIST:
            self.number2Pic[number] = self.resizeImage(number)

    def resizeImage(self, number):
        fileName = 'images/' + str(number) + '.GIF'
        pilImage = Image.open(fileName).resize((self.IMAGE_SIZE,self.IMAGE_SIZE))
        #设置成成员变量
        self.tkImage = ImageTk.PhotoImage(image=pilImage)
        return self.tkImage

    def moveUp(self):
        t = copy.deepcopy(self.map)
        for i in range(self.GRID_NUMBER):
            for j in range(self.GRID_NUMBER - 1):
                for k in range(j+1,self.GRID_NUMBER):
                    if self.map[k][i] > 0:
                        #下一行为0
                        if self.map[j][i] == 0:
                            self.map[j][i] = self.map[k][i]
                            self.map[k][i] = 0
                        elif self.map[j][i] == self.map[k][i]:
                            self.map[j][i] *= 2
                            self.score += self.map[j][i]
                            self.map[k][i] = 0
                        break
        if not operator.eq(t, self.map):
            self.getNewNumber(1)
            self.updateMap()

    def moveDown(self):
        t = copy.deepcopy(self.map)
        #i是列数
        for i in range(self.GRID_NUMBER):
            for j in range(self.GRID_NUMBER - 1,0,-1):
                for k in range(j-1,-1,-1):
                    #上一行不为0
                    if self.map[k][i] > 0:
                        #下一行为0
                        if self.map[j][i] == 0:
                            self.map[j][i] = self.map[k][i]
                            self.map[k][i] = 0
                        elif self.map[j][i] == self.map[k][i]:
                            self.map[j][i] *= 2
                            self.score += self.map[j][i]
                            self.map[k][i] = 0
                        break

        if not operator.eq(t, self.map):
            self.getNewNumber(1)
            self.updateMap()

    def moveLeft(self):
        t = copy.deepcopy(self.map)
        for i in range(self.GRID_NUMBER):
            for j in range(self.GRID_NUMBER - 1):
                for k in range(j+1, self.GRID_NUMBER):
                    if self.map[i][k] > 0:
                        if self.map[i][j] == 0:
                            self.map[i][j] = self.map[i][k]
                            self.map[i][k] = 0
                        elif self.map[i][j] == self.map[i][k]:
                            self.map[i][j] *= 2
                            self.score += self.map[i][j]
                            self.map[i][k] = 0
                        break
        if not operator.eq(t,self.map):
            self.getNewNumber(1)
            self.updateMap()

    def moveRight(self):
        t = copy.deepcopy(self.map)
        for i in range(self.GRID_NUMBER):
            for j in range(self.GRID_NUMBER - 1,0,-1):
                for k in range(j-1,-1,-1):
                    if self.map[i][k] > 0:
                        if self.map[i][j] == 0:
                            self.map[i][j] = self.map[i][k]
                            self.map[i][k] = 0
                        elif self.map[i][j] == self.map[i][k]:
                            self.map[i][j] *= 2
                            self.score += self.map[i][j]
                            self.map[i][k] = 0
                        break
        if not operator.eq(t,self.map):
            self.getNewNumber(1)
            self.updateMap()

    def printMap(self):
        for item in self.map:
            print(item)
        print()

    def getNewNumber(self, times):
        #times表示一次生成多少个随机数
        for i in range(times):
            random_x = random.randint(0,self.GRID_NUMBER-1)
            random_y = random.randint(0, self.GRID_NUMBER - 1)

            while self.map[random_x][random_y] != 0:
                random_x = random.randint(0, self.GRID_NUMBER - 1)
                random_y = random.randint(0, self.GRID_NUMBER - 1)


            self.map[random_x][random_y] = 2 if random.randint(0,10) > 2 else 4


    def getState(self):
        #游戏胜利
        for item in self.map:
            if self.PASS_CONDITION in item:
                return 1
        #游戏可以继续进行
        for item in self.map:
            if 0 in item:
                return 0

        can1 = False
        can2 = False
        for j in range(self.GRID_NUMBER):
            for i in range(self.GRID_NUMBER - 1):
                if self.map[i][j] == self.map[i+1][j]:
                    can1 = True

        for i in range(self.GRID_NUMBER):
            for j in range(self.GRID_NUMBER - 1):
                if self.map[i][j] == self.map[i][j+1]:
                    can2 = True
        if can1 or can2:
            return 0

        #游戏结束
        return -1

    def check(self):
        if self.getState() == 1:
            print('Win')
            restart = messagebox.askyesno('提示', '胜利！点击是重来')
            if restart:
                self.initMap()
            else:
                sys.exit()
        if self.getState() == -1:
            print('Good Game')
            restart = messagebox.askyesno('提示', '失败！点击是重来')
            if restart:
                self.initMap()
            else:
                sys.exit()
    def main(self,event):
        direction = event.keysym
        # directions = ['Up','Down','Left','Right']
        # for i in range(100000):
        #     for direction in directions:
        if direction == 'Up':
            self.moveUp()
            self.printMap()
            self.check()
        elif direction == 'Down':
            self.moveDown()
            self.printMap()
            self.check()
        elif direction == 'Left':
            self.moveLeft()
            self.printMap()
            self.check()
        elif direction == 'Right':
            self.moveRight()
            self.printMap()
            self.check()
        elif direction == 'space':
            self.initMap()
            self.printMap()


if __name__ == '__main__':
    game = Game2048()
    game.window.mainloop()

