import pygame
import numpy as np
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

BLOCK_SIZE = 20
WIDTH = 20
HEIGHT = 20
SPEED = 60
WIN_WIDTH = WIDTH*BLOCK_SIZE
WIN_HEIGHT = HEIGHT*BLOCK_SIZE

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Snake Game')


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

class Snake:
    def __init__(self):

        self.clock = pygame.time.Clock()
        self.reset()
    
    def reset(self):

        self.direction = Direction.RIGHT

        self.head = Point(WIN_WIDTH/2, WIN_HEIGHT/2)
        self.snake = [self.head,
                      Point(self.head.x - BLOCK_SIZE, self.head.y),
                      Point(self.head.x - 2*BLOCK_SIZE, self.head.y)]

        self.score = 0
        self.food = None
        self.frame_iteration = 0

        self._place_food()

    def _place_food(self):
        x = random.randint(0, (WIN_WIDTH-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (WIN_HEIGHT - BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self, action):

        self.frame_iteration += 1

        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        if action == 0:
            self.direction = Direction.LEFT
        elif action == 1:
            self.direction = Direction.RIGHT
        elif action == 2:
            self.direction = Direction.UP
        elif action == 3:
            self.direction = Direction.DOWN

        # 2. move
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # 3. check if gameover
        game_over = False
        if self._is_collide() or self.frame_iteration > 50*len(self.snake):
            game_over = True
            return game_over, self.score
        
        self.score += 2

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 10
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(
                pt.x+4, pt.y+4, BLOCK_SIZE-8, BLOCK_SIZE-8))

        pygame.draw.rect(self.display, RED, pygame.Rect(
            self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score : " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
        

    def _is_collide(self):

        # Solid Walls
        if self.head.x > WIN_WIDTH - BLOCK_SIZE or self.head.x < 0 or self.head.y > WIN_HEIGHT - BLOCK_SIZE or self.head.y < 0:
            return True

        if self.head in self.snake[1:]:
            return True

        return False
    
    def get_head(self):
        x = self.head.x/WIDTH
        y = self.head.y/HEIGHT
        return (x,y)
    
    def get_food(self):
        x = self.food.x/WIDTH
        y = self.food.y/HEIGHT
        return (x,y)
    


