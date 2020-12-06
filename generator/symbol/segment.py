#!/usr/bin/env python

import sys
import random
import argparse
import colorsys
# import and init pygame
import pygame
pygame.init()


'''
Draws a grid of random color pixels, finds near colors using a distance metric,
and draws an edge between the two pixels if one is the nearest neighbor of the other.

TODO:
- RGB values for colors are too large

- second pass: check neighbors for membership in the same group; might
  help with jagged edges

'''

BLACK = [0, 0, 0]
WHITE = [0xFF, 0xFF, 0xFF]


def distance(grid, x0, y0, x1, y1):
    c0 = grid[x0][y0]
    c1 = grid[x1][y1]
    dist = (abs(c0[0]-c1[0]) + abs(c0[1]-c1[1]) + abs(c0[2]-c1[2]))/3/255
    return dist

def average(grid, x0, y0, x1, y1):
    c0 = grid[x0][y0]
    c1 = grid[x1][y1]
    avg = c0.lerp(c1, 0.5)
    return avg

def random_pixels(pixels):
    grid = []
    for x in range(pixels):
        grid.append([])
        for y in range(pixels):
            hue = random.uniform(0.0, 1.0)
            sat = 1.0
            val = 1.0
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            rgb = (rgb[0]*255, rgb[1]*255, rgb[2]*255)
            grid[x].append(pygame.Color(rgb))

    links = []
    for x in range(pixels):
        for y in range(pixels):

            neighbors = []
            if x > 0:
                neighbors.append((x-1, y))
            if x < pixels-1:
                neighbors.append((x+1, y))
            if y > 0:
                neighbors.append((x, y-1))
            if y < pixels-1:
                neighbors.append((x, y+1))
            nearest = None
            nearest_dist = 100
            thresh = 0.5
            for neigh in neighbors:
                dist =  distance(grid, *(x,y), *neigh)
                if dist < thresh and dist < nearest_dist:
                    nearest = neigh
                    nearest_dist = dist
            if nearest:
                links.append([(x, y), nearest])
    return grid, links

def block_draw(window, grid, links, size, scale):
    pixels = size // scale
    for x in range(pixels):
        for y in range(pixels):
            x0 = x*scale
            x1 = x*scale + scale
            y0 = y*scale
            y1 = y*scale + scale
            try:
                pygame.draw.rect(window, grid[x][y], [x0, y0, x1, y1])
            except:
                print(x, y, grid[x][y])

    for link in links:
        x0, y0 = link[0]
        x1, y1 = link[1]
        color = average(grid, x0, x1, y0, y1)
        pygame.draw.line(window, color,
                         ((x0+0.5)*scale, (y0+0.5)*scale),
                         ((x1+0.5)*scale, (y1+0.5)*scale), width=8)


def image_window(size, scale):
    pixels = size // scale
    grid, links = random_pixels(pixels)

    # create the screen
    window = pygame.display.set_mode((size, size))
    bg_color = BLACK
    pygame.display.get_surface().fill(bg_color)

    block_draw(window, grid, links, width, scale)

    # draw all symbols at once
    pygame.display.flip()


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='symbol generator')
    # parser.add_argument('--width', action='store', type=int, default=3,
    #                     help='width of symbols')
    # parser.add_argument('--scale', action='store', type=int, default=10,
    #                     help='space between points and padding around symbols, in pixels')

    #args = parser.parse_args()

    # scale = args.scale
    # width = args.width
    # colors = args.colors

    width = 400
    scale = 50

    image_window(width, scale)

    # keep window open
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                pass
