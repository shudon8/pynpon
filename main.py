import math
from random import randint
from typing import Self
import pygame as pg

pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
velocityMultiplier = 1
def main():
    done = False
    table = Table(640, 480)
    pinpon = Ball(table.width, table.height, 10, (255, 255, 255))
    player1 = Player(0, table)
    player2 = Player(1, table)
    while not done:
        done = tick(pinpon, table, player1, player2)
        screen.fill((50, 50, 50))

    pg.quit()

def tick(pinpon, table, player1, player2):
    pg.event.pump()
    keys = pg.key.get_pressed()
    if keys[pg.K_ESCAPE] or keys[pg.K_q] or pg.event.peek(pg.QUIT):
        return True
    
    if(keys[pg.K_LEFT]):
        if player1.x > 0:
            player1.x -= 5
    if(keys[pg.K_RIGHT]):
        if player1.x < table.width - player1.width:
            player1.x += 5    
    if(keys[pg.K_a]):
        if player2.x > 0:
            player2.x -= 5
    if(keys[pg.K_d]):
        if player2.x < table.width - player2.width:
            player2.x += 5
    # draw ball
    pinpon.move()

    if pinpon.location[0] <= pinpon.radius or pinpon.location[0] >= table.width - pinpon.radius:
        pinpon.velocity[0] *= -1
    if pinpon.location[1] <= pinpon.radius or pinpon.location[1] >= table.height - pinpon.radius:
        pinpon.velocity[1] *= -1

    p1y = player1.y <= pinpon.location[1] + pinpon.radius
    p1x = player1.x <= pinpon.location[0] and pinpon.location[0] <= player1.x + player1.width + pinpon.radius
    if p1y and p1x:
        pinpon.hit(pinpon.location[0], player1.x + player1.width / 2)

    p2y = player2.y >= pinpon.location[1] - pinpon.radius
    p2x = player2.x <= pinpon.location[0] and pinpon.location[0] <= player2.x + player2.width + pinpon.radius
    if p2y and p2x:
        pinpon.hit(pinpon.location[0], player2.x + player2.width / 2)

    pg.draw.circle(screen, pinpon.color, (pinpon.location[0], pinpon.location[1]), pinpon.radius)

    # draw players
    pg.draw.rect(screen, (255, 255, 255), (player1.x, player1.y, player1.width, player1.height))
    pg.draw.rect(screen, (255, 255, 255), (player2.x, player2.y, player2.width, player2.height))
    pg.display.flip()
    clock.tick(60)
    return False

class Table():
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Player():
    def __init__(self, player_number, table):
        self.x = table.width / 2
        if player_number == 1:
            self.y = 10
        else:
            self.y = table.height - 10
        self.width = 100
        self.height = 5

class Ball():
    def __init__(self, width, height, radius, color):
        self.radius = radius
        self.color = color
        self.location = [width / 2, height / 2]
        self.velocity = [-0, 3]
    
    def hit(self, player_hit_location, player_location_x):
        global velocityMultiplier
        self.velocity[0] = ((self.location[0] - player_location_x) / 10) * velocityMultiplier
        self.velocity[1] *= -1
        velocityMultiplier += 0.5
        if abs(self.velocity[0]) >= 0 and abs(self.velocity[0]) < 1:
            pg.mixer.music.load('sounds/slow.wav')
            pg.mixer.music.play(0)
        elif abs(self.velocity[0]) >= 1 and abs(self.velocity[0]) < 2.5:
            pg.mixer.music.load('sounds/mid.wav')
            pg.mixer.music.play(0)
        elif abs(self.velocity[0]) >= 2.5:
            pg.mixer.music.load('sounds/fast.wav')
            pg.mixer.music.play(0)
        
    def move(self):
        self.location[0] += self.velocity[0]
        self.location[1] += self.velocity[1]

main()