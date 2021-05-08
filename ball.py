import time
import random
xmid = 250
ymid = 200
speed = 2
timestep = 1
leftborder = 0
rightborder = 500
paddleheight = 40
paddlewidth = 20 #afstand van rechterkant paddle tot border
top = 0
bottom = 400
class ball:

    
    def __init__(self):
        print("Ball made")
        self.xpos = xmid
        self.ypos = ymid
        self.dx = 0
        self.dy = 0
        self.starttime = time.time()
        self.goal = False
        self.scorer = 1
        
    def update(self, paddle0,paddle1):
        #deltat = time.time() - self.starttime
        self.xpos += self.dx#round(self.dx * deltat)
        self.ypos += self.dy#round(self.dy * deltat)
        if self.xpos >= leftborder + paddlewidth and self.xpos <= leftborder + paddlewidth + 5 and self.ypos >= paddle0 and self.ypos <= paddle0 + paddleheight and self.dx <=0:
            print("Ball botst links")
            self.dx *= -1
        if self.xpos <= rightborder - paddlewidth and self.xpos >= rightborder - paddlewidth - 5 and self.ypos >= paddle1 and self.ypos <= paddle1 + paddleheight and self.dx >=0:
            print(str(self.xpos) + " <= " + str(rightborder - paddlewidth) + " and " + str(self.xpos) + " >= " + str(leftborder - paddlewidth - 5) + " and " + str(self.ypos) + " >= " + str(paddle1) + " and " + str(self.ypos) + " <= " + str(paddle1 + paddleheight) + " and "+str(self.dy)+" >= "+ str(0))
            print("Ball botst rechts")
            #print("richting ="+self.dx)
            self.dx *= -1
            print("richting ="+str(self.dx))
        if self.xpos < leftborder:
            print("Goal links")
            self.scorer = 0
            self.goal = True
        elif self.xpos > rightborder:
            print(str(self.xpos) + " <= " + str(rightborder - paddlewidth) + " and " + str(self.xpos) + " >= " + str(leftborder - paddlewidth - 5) + " and " + str(self.ypos) + " >= " + str(paddle1) + " and " + str(self.ypos) + " <= " + str(paddle1 + paddleheight) + " and "+str(self.dy)+" >= "+ str(0))
            print("Goal rechts")
            self.scorer = 1
            self.goal = True
        elif self.ypos < top:
            print("Ball boven")
            self.dy *= -1
        elif self.ypos > bottom:
            print("Ball beneden")
            self.dy *= -1
            
    def reset(self):
        self.xpos = xmid
        randomy = random.randint(top+2,bottom-2)
        self.ypos = randomy
        #self.ypos = ymid
        self.dx = 0
        self.dy = 0
        time.sleep(3.5)
        if self.scorer == 0:
            self.dx = -speed
        else:
            self.dx = speed
        self.dy = speed
