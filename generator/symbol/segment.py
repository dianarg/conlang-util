#!/usr/bin/env python

import sys
import random
import argparse
import colorsys
import numpy as np
import skimage
import skimage.io
import skimage.transform
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
    #color = BLACK
    c0 = pygame.Color(grid[x0][y0])
    c1 = pygame.Color(grid[x1][y1])
    color = c0.lerp(c1, 0.5)
    color = pygame.Color([255 - color.r, 255 - color.g, 255 - color.b])
    return color


def find_links(grid):
    wpixels = len(grid)
    links = []
    for x in range(wpixels):
        # these should all be the same
        hpixels = len(grid[x])
        for y in range(hpixels):

            neighbors = []
            if x > 0:
                neighbors.append((x-1, y))
            if x < wpixels-1:
                neighbors.append((x+1, y))
            if y > 0:
                neighbors.append((x, y-1))
            if y < hpixels-1:
                neighbors.append((x, y+1))
            thresh = 0.04
            for neigh in neighbors:
                dist =  distance(grid, *(x,y), *neigh)
                if dist < thresh:
                    links.append([(x, y), neigh])
    return links

def random_pixels(wpixels, hpixels):
    grid = []
    for x in range(wpixels):
        grid.append([])
        for y in range(hpixels):
            hue = random.uniform(0.0, 1.0)
            sat = 1.0
            val = 1.0
            rgb = colorsys.hsv_to_rgb(hue, sat, val)
            rgb = (rgb[0]*255, rgb[1]*255, rgb[2]*255)
            grid[x].append(pygame.Color(rgb))

    return grid

def block_draw(window, grid, links, wpixels, hpixels, scale):
    for x in range(wpixels):
        for y in range(hpixels):
            x0 = x*scale
            x1 = x*scale + scale
            y0 = y*scale
            y1 = y*scale + scale
            try:
                pygame.draw.rect(window, grid[x][y], [x0, y0, x1, y1])
            except:
                print(x, y, grid[x][y])

    pen_width = scale // 2
    for link in links:
        x0, y0 = link[0]
        x1, y1 = link[1]
        color = average(grid, x0, y0, x1, y1)
        pygame.draw.line(window, color,
                         ((x0+0.5)*scale, (y0+0.5)*scale),
                         ((x1+0.5)*scale, (y1+0.5)*scale), width=pen_width)


def load_image(image_path, wpixels, hpixels):

    img = skimage.io.imread(args.image).astype(np.uint8)
    # fix rotation
    img = np.transpose(img, (1, 0, 2))

    # apply scale to pixelize
    img = skimage.transform.resize(img, (wpixels, hpixels))

    # RGB for pygame
    img *= 255

    return img.tolist()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='symbol generator')
    parser.add_argument('--image', '-i', action='store', type=str, default=None)
    parser.add_argument('--scale', action='store', type=int, default=10,
                        help='size of image pixels in screen pixels')

    args = parser.parse_args()

    width = 800
    height = 800
    scale = args.scale
    wpixels = width // scale
    hpixels = height // scale

    # create the screen
    width = wpixels * scale
    height = hpixels * scale
    window = pygame.display.set_mode((width, height))
    bg_color = BLACK
    pygame.display.get_surface().fill(bg_color)

    grid = None
    if args.image:
        grid = load_image(args.image, wpixels, hpixels)
        # TODO: check size
    else:
        wpixels = width // scale
        hpixels = height // scale
        grid = random_pixels(wpixels, hpixels)

    if grid is not None:
        links = find_links(grid)
        block_draw(window, grid, links, wpixels, hpixels, scale)

    # draw all symbols at once
    pygame.display.flip()

    # keep window open
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                pass
