import cv2
import numpy as np
import pygame
import sys
from pygame.locals import *

width = 800
height = 500
#Tao khung hien thi game
display_surf = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

WHITE = (255, 255, 255)
# pygame.draw.line(display_surf, WHITE, (width/2, 0), (width/2, height), 3)
# pygame.draw.rect(display_surf, WHITE, (10, 10, 20, 20))
fps = 200 #so frame tren giay
fps_clock = pygame.time.Clock()

# Create an object capture
cap = cv2.VideoCapture(0)
# Create an identify object
classhar = cv2.CascadeClassifier("C:\\Users\\ASUS\\Downloads\\haarcascade_frontalface_default (1).xml")
# load mask
# mask = cv2.imread("E:\\AI files\\C4T_main_module\\1.jpg")


class Paddle:

    def __init__(self, w, h, x, y):
        self.width = w
        self.height = h
        self.x = x
        self.y = y

    def Draw(self):
        pygame.draw.rect(display_surf, WHITE, (self.x, self.y, self.width, self.height))

    def Move(self, pos):
        self.y = pos[1] - self.height/2
        if self.y < 0:
            self.y = 0
        if self.y > height - self.height:
            self.y = height - self.height


class AutoPaddle(Paddle):

    def __init__(self, w, h, x, y, speed):
        super().__init__(w, h, x, y)
        self.speed = speed

    def AutoMove(self, ball):
        self.y = ball.y - self.height/2
        if self.y < 0:
            self.y = 0
        if self.y > height - self.height:
            self.y = height - self.height


class Ball:

    def __init__(self, w, h, x, y, speed):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.speed = speed
        self.dir_x = 1 # 1 right and -1 left
        self.dir_y = 1 # 1 down and -1 up

    def Draw(self):
        pygame.draw.rect(display_surf, WHITE, (self.x, self.y, self.width, self.height))

    def Move(self):
        self.x = self.x + self.dir_x * self.speed
        self.y = self.y + self.dir_y * self.speed

    def Bounce(self, axis):
        if axis == "x":
            self.dir_y = self.dir_y * -1
        if axis == "y":
            self.dir_x = self.dir_x * -1

    def HitCeiling(self):
        if self.y <= 0 or self.y >= (height - self.height):
            return True
        else:
            return False

    def HitPaddle(self, paddle):
        if (paddle.y - self.height) <= self.y <= (paddle.y + paddle.height) and self.x <= (paddle.x + paddle.width):
            return True
        else:
            return False

    def HitAutoPaddle(self, autopaddle):
        if (autopaddle.y - self.height) <= self.y <= (autopaddle.y + autopaddle.height) and (self.x + self.width) >= autopaddle.x:
            return True
        else:
            return False


class ScoreBoard:

    def __init__(self, x, y, score, size):
        self.x = x
        self.y = y
        self.score = score
        self.size = size
        self.font = pygame.font.Font(None, self.size)

    def Display(self):
        display_score = self.font.render("Score: " + str(self.score), True, WHITE)
        display_surf.blit(display_score, (self.x, self.y))


class Game:

    def __init__(self, ball, paddle, autopaddle, scoreboard, speed):
        self.speed = speed
        self.ball = ball
        self.paddle = paddle
        self.autopaddle = autopaddle
        self.scoreboard = scoreboard

    def DrawArena(self):
        display_surf.fill((0, 0, 0))
        pygame.draw.line(display_surf, WHITE, (width/2, 0), (width/2, height), 3)
        self.ball.Draw()
        self.paddle.Draw()
        self.autopaddle.Draw()
        self.scoreboard.Display()

    def Update(self, pos):
        if self.ball.HitCeiling():
            self.ball.Bounce("x")
        if self.ball.HitAutoPaddle(self.autopaddle):
            self.ball.Bounce("y")
        if self.ball.HitPaddle(self.paddle):
            self.ball.Bounce("y")
            self.scoreboard.score += 1
        self.ball.Move()
        self.paddle.Move(pos)
        self.autopaddle.AutoMove(self.ball)


def Main():
    pygame.init()
    ball = Ball(10, 10, 10, 10, 1)
    paddle = Paddle(20, 50, 10, height/2)
    autopaddle = AutoPaddle(20, 50, width - 10, height/2, 1)
    scoreboard = ScoreBoard(150, 20, 0, 20)
    game = Game(ball, paddle, autopaddle, scoreboard, 1)
    mousepos = [10, 10]
    die = False



    while True:

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Detect face
        faces = classhar.detectMultiScale(gray)

        HImage = frame.shape[0]

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Detect face
        faces = classhar.detectMultiScale(gray)

        x_max = 0
        y_max = 0
        w_max = 0
        h_max = 0

        for x, y, w, h in faces:
            if (w * h) > (w_max * h_max):
                x_max = x
                y_max = y
                w_max = w
                h_max = h

        k = float(height) / HImage

        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                die = True

        mousepos = (int(x_max), int((float(height) / (HImage - 40)) * y_max))


        if ball.x <= 0 and ball.HitPaddle(paddle) is False:
            die = True

        game.DrawArena()
        game.Update(mousepos)
        pygame.display.update()
        fps_clock.tick(fps)

        if die:
            break

        cv2.imshow("img", frame)

        k = cv2.waitKey(30)

        if k == 27:
            cap.release()
            break
        elif k == ord('s') & 0xFF:
            cv2.imwrite('img.jpg', frame)
            cap.release()
            break
    # while True:
    #     display_surf.fill((0, 0, 0))
    #     font = pygame.font.Font(None, 100)
    #     display_score = font.render("Ngu", True, WHITE)
    #     display_surf.blit(display_score, (width/2, height/2))
    #     for event in pygame.event.get():
    #     if event.type == KEYDOWN:
    #         pygame.quit()
    #         sys.exit()


if __name__ == '__main__':
    Main()