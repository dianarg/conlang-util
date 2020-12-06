#!/usr/bin/env python
# Toy Terrain Generator

import sys
# import and init pygame
import pygame
import random
pygame.init()


class PixelGrid:
    def __init__(self, size, scale):
        self.points = []
        self.size = size
        self.scale = scale
        for i in range(size):
            self.points.append([])
            for j in range(size):
                self.points[i].append(base_height)

    def normalize(self):
        min = self.points[0][0]
        max = min
        for i in range(self.size):
            for j in range(self.size):
                if (self.points[i][j] < min):
                    min = self.points[i][j]
                if (self.points[i][j] > max):
                    max = self.points[i][j]

        for i in range(self.size):
            for j in range(self.size):
                self.points[i][j] -= min
                self.points[i][j] = ((self.points[i][j]*1.0)/max)*255
                if(self.points[i][j] > 255):
                    self.points[i][j] = 255
                if (self.points[i][j] < 0):
                    self.points[i][j] = 0

    def apply_threshold(self, height):
        color = (height, height, height)
        if do_threshold:
            if height > 200:
                color = color  # grey for snow
            elif height > 150:
                color = (height/2, height/3, height/3)  # brown
            elif height > 75:
                color = (0, 255-height, 0)  # green
            elif height > 70:
                color = (height*2, height*2, 0)  # beach yellow
            else:
                color = (0, 0, height)   # blue to black
        return color

    def draw(self, apply_threshold=True):
        for i in range(self.size):
            for j in range(self.size):
                hc = self.points[i][j]
                color = self.apply_threshold(hc)
                pygame.draw.rect(window, color, (self.scale * i,
                                                 self.scale * j,
                                                 self.scale * i + self.scale,
                                                 self.scale * j + self.scale))

        # draw it to the screen
        pygame.display.flip()

    def random_heights(self):
        for i in range(self.size):
            for j in range(self.size):
                self.points[i][j] = random.randint(0, 255)

    def diamond_square(self):
        block = self.size
        size = self.size
        d = int(size/4)
        self.points[0][0] = random.randint(0, 255)
        self.points[size-1][size-1] = random.randint(0, 255)
        self.points[0][size-1] = random.randint(0, 255)
        self.points[size-1][0] = random.randint(0, 255)
        while block > 1:
            # average four corners
            i = 0
            off = block/2

            while i < self.size:
                j = 0
                while j < self.size:
                    self.points[i+off][j+off] = (
                        self.points[i][j] +
                        self.points[(i+block) % size][j] +
                        self.points[i][(j+block) % size] +
                        self.points[(i+block) % size][(j+block) % size]
                    )/4 + random.randint(-d, d)
                    j += block
                i += block
            # average edges
            i = 0
            off = block/2
            while i < self.size:
                j = 0
                while j < self.size:
                    self.points[i][j+off] = (
                        self.points[i][j] +
                        self.points[i][(j+block) % size] +
                        self.points[(i+off) % size][(j+off) % size] +
                        self.points[(i-off) % size][(j+off) % size]
                    )/4 + random.randint(-d, d)
                    self.points[i+off][j] = (
                        self.points[i][j] +
                        self.points[(i+off) % size][(j+off) % size] +
                        self.points[(i+block) % size][j] +
                        self.points[(i+off) % size][(j-off) % size]
                    )/4 + random.randint(-d, d)
                    j += block
                i += block
            block = block/2
            d = int(d/2.2)


if __name__ == '__main__':
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # create the screen
    # pixel grid parameters
    grid_size = 512
    base_height = 127
    scale = 1
    screen_size = scale * grid_size
    window = pygame.display.set_mode((screen_size, screen_size))
    font = pygame.font.Font(None, 17)
    grid = PixelGrid(grid_size, scale)

    pygame.display.get_surface().fill(BLACK)
    text = font.render('Press any key to generate a new map.', True, WHITE)
    textrect = text.get_rect()
    textrect.centerx = window.get_rect().centerx
    textrect.centery = window.get_rect().centery
    window.blit(text, textrect)
    pygame.display.update()

    # whether to make thresholded map or heightmap
    do_threshold = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                pygame.display.get_surface().fill(BLACK)
                print('diamond square...')
                grid.diamond_square()
                print('normalize...')
                grid.normalize()
                print('draw...')
                grid.draw(do_threshold)
                print('done!')
