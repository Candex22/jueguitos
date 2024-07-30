import pygame,sys
from pygame.math import Vector2
import random
import mysql.connector
from mysql.connector import Error
import time

pygame.init()
height = 480
width = 720
win = pygame.display.set_mode((width, height))

class Paleta():
    def __init__(self) -> None:
        self.body = [Vector2(10, 100), Vector2(10, 110), Vector2(10, 120), Vector2(10, 120)]
        self.direction = Vector2(10, 0)
        pygame.draw.rect(10,10)

    def move_up(self):
        self.direction = Vector2(0, -10)
        
    def move_down(self):
        self.direction = Vector2(0, 10)
    
def main():
    paleta = Paleta()

    while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            if event.type == pygame.KEYDOWN and paleta.direction.y != 10:
                if event.key == pygame.K_UP:
                    paleta.move_up()

            if event.type == pygame.KEYDOWN and paleta.direction.y != -10:
                if event.key == pygame.K_DOWN:
                    paleta.move_down()
            pygame.display.update()

main()
