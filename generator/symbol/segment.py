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
            nearest = None
            nearest_dist = 100
            next_nearest = None
            next_nearest_dist = 100
            thresh = 0.04
            for neigh in neighbors:
                dist =  distance(grid, *(x,y), *neigh)
                if dist < thresh:
                    links.append([(x, y), neigh])

            #     if dist < thresh and dist < nearest_dist:
            #         nearest = neigh
            #         nearest_dist = dist
            #     if dist < thresh and next_nearest != nearest and dist < next_nearest_dist:
            #         next_nearest = neigh
            #         next_nearest_dist = dist
            # if nearest:
            #     links.append([(x, y), nearest])
            # if next_nearest:
            #     links.append([(x,y), next_nearest])
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
        color = BLACK
        pygame.draw.line(window, color,
                         ((x0+0.5)*scale, (y0+0.5)*scale),
                         ((x1+0.5)*scale, (y1+0.5)*scale), width=pen_width)


def load_image(image_path, wpixels, hpixels):
    img = pygame.image.load(image_path)
    img = pygame.transform.smoothscale(img, (wpixels, hpixels))
    #img.convert()
    img = pygame.surfarray.array2d(img)
    pix = []
    for ww in img:
        pix.append([])
        for hh in ww:
            try:
                res = pygame.Color('#{:06x}'.format(hh))
            except:
                print(hh, '#{:06x}'.format(hh))
            pix[-1].append(res)
    return pix

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='symbol generator')
    parser.add_argument('--image', '-i', action='store', type=str, default=None)
    # parser.add_argument('--width', action='store', type=int, default=3,
    #                     help='width of symbols')
    # parser.add_argument('--scale', action='store', type=int, default=10,
    #                     help='space between points and padding around symbols, in pixels')

    args = parser.parse_args()

    # scale = args.scale
    # width = args.width
    # colors = args.colors
    width = 800
    height = 800
    scale = 40
    wpixels = width // scale
    hpixels = height // scale

    if args.image:
        grid = load_image(args.image, wpixels, hpixels)
        # TODO: check size
    else:
        wpixels = width // scale
        hpixels = height // scale
        grid = random_pixels(wpixels, hpixels)

    links = find_links(grid)

    # create the screen
    width = wpixels * scale
    height = hpixels * scale
    window = pygame.display.set_mode((width, height))
    bg_color = BLACK
    pygame.display.get_surface().fill(bg_color)

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
