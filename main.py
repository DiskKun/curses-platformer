import curses
import sys
import time
from curses import wrapper
window = curses.initscr()
curses.curs_set(0)
window.nodelay(True)
# CONSTANTS
P_GRAV = .01
P_ACCEL = .1
P_FRIC = .02
P_J_ACCEL = -.5

class GameObject:
    instances = []
    def __init__(self, x, y, c, t, vx=0):
        # VARS
        self.x = x
        self.y = y
        self.ix = x
        self.iy = y
        self.ivx = vx
        self.c = c
        self.t = t
        self.veloy = 0
        self.velox = vx
        self.onGround = False
        self.isJumping = True
        self.__class__.instances.append(self)

def main(stdscr):
    game_over = False
    player = GameObject(curses.COLS/2, curses.LINES/2, "@", "Player")
    enemy1 = GameObject(curses.COLS/4*3, curses.LINES/2, "&", "Enemy", 0.1)
    window.clear()

    def drawObjects():
        for instance in GameObject.instances:
            window.addstr(int(round(instance.y)), int(round(instance.x)), instance.c)

    def drawScene():
        window.border("#", "#", "#", "#", "#", "#", "#", "#")
        window.hline(int(round(curses.LINES/4*3)), int(round(curses.COLS/10)), "#", 5)
        window.vline(int(round(curses.LINES/4*2)), int(round(curses.COLS/10)), "#", 5)

    def applyFric():
        player.veloy = P_GRAV+player.veloy
        if player.veloy > 1:
            player.veloy = 1
        if player.velox > 0:
            player.velox -= P_FRIC
        elif player.velox < 0:
            player.velox += P_FRIC
        for instance in GameObject.instances:
            if instance.t == "Enemy":
                instance.veloy += P_GRAV

    def updatePosition():
        for instance in GameObject.instances:
            tempy = instance.y
            tempx = instance.x
            tempy += round(instance.veloy, 3)
            tempx += round(instance.velox, 3)
            moveToY = window.inch(int(round(tempy)), int(round(instance.x)))
            moveToX = window.inch(int(round(instance.y)), int(round(tempx)))
            moveTo = window.inch(int(round(instance.y)), int(round(instance.x)))
            if moveToX == 32:
                instance.x = instance.x + round(instance.velox, 3)
            elif moveToX == 35:
                if instance.t == "Player":
                    instance.velox = 0
                elif instance.t == "Enemy":
                    instance.velox = -instance.velox
            if moveToY == 32:
                instance.y = instance.y + round(instance.veloy, 3)
                instance.onGround = False
            elif moveToY == 35:
                instance.veloy = 0
                instance.onGround = True
            t1 = instance.t
            x1 = int(round(instance.x))
            y1 = int(round(instance.y))
            for instance2 in GameObject.instances:
                t2 = instance2.t
                x2 = int(round(instance2.x))
                y2 = int(round(instance2.y))
                if t1 == "Player" and t2 == "Enemy":
                    if y1 == y2 and x1 == x2:
                        gameOver()

    def roundOff():
        for instance in GameObject.instances:
            instance.velox = round(instance.velox, 3)
            instance.veloy = round(instance.veloy, 3)

    def inputHandle():
        key = window.getch()
        if key == curses.KEY_UP:
            if player.onGround == True:
                player.veloy = P_J_ACCEL
        if key == curses.KEY_LEFT:
            player.velox -= P_ACCEL
            if player.velox < -1:
                player.velox = -1
        elif key == curses.KEY_RIGHT:
            player.velox += P_ACCEL
            if player.velox > 1:
                player.velox = 1

    def gameOver():
        window.addstr(int(curses.LINES/2), int(curses.COLS/2-4), "GAME OVER")
        window.nodelay(False)
        window.getkey()
        window.nodelay(True)
        for instance in GameObject.instances:
            instance.y = instance.iy
            instance.x = instance.ix
            instance.velox = instance.ivx



    while game_over == False:
        curses.update_lines_cols()
        inputHandle()
        window.clear()
        drawScene()
        applyFric()
        roundOff()
        updatePosition()
        drawObjects()
        window.refresh()
        time.sleep(1/120)
wrapper(main)
