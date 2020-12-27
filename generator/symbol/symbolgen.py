#!/usr/bin/env python

import sys
import random
import argparse
import colorsys
# import and init pygame
import pygame
pygame.init()

'''
# Examples:
  Draw random symbols with the default values.
    ./symbolgen.py
  Draw random symbols in 3x3 grid, use 4 points per side, scale 20, and showing
  stroke order with colors.
    ./symbolgen.py --width=4 --scale=20 --num_symbol=3 --colors


# Description
Experiment with graphs to draw symbols in a certain style.

Nodes are numbered across rows and graph edges are to immediate neighbors,
including diagonals. A symbol can be represented by a list of node numbers to
connect with lines, in order.
For aethetic reasons, the line should not pass through the same node twice.

n = 5
0 1 2 3 4
5 6 7 8 9
a b c d e
f g h i j
k l m n o

n = 3
0 1 2
3 4 5
6 7 8

If n=3, code 0,4,8 would generate a line from the top left to the lower right corner.
Code 0,2,6 would make a shape like a 7.

'''


def num_to_symbol(width, num_str):
    if width > 6:
        raise ValueError('cannot handle integer base over 36')
    symbol = []
    for cc in num_str:
        symbol.append(int(cc, width*width))
    return symbol


def point_list_to_segments(plist):
    lines = []
    first = plist.pop()
    while len(plist) > 0:
        next = plist.pop()
        lines.append((next, first))
        first = next
    lines.reverse()
    return lines


def color_list(num_seg):
    saturation = 1.0
    value = 1.0
    spacing = 1.0 / num_seg
    colors = []
    for i in range(num_seg):
        hue = i * spacing
        rgb = colorsys.hsv_to_rgb(hue, saturation, value)
        rgb = (rgb[0]*255, rgb[1]*255, rgb[2]*255)
        colors.append(rgb)
    return colors


def rainbow_block_draw(window, plist, x, y, width, scale):
    block_draw_segment(window, plist, x, y, width, scale, True)


def block_draw_segment(window, plist, x, y, width, scale, use_color):
    assert len(plist) > 0
    if len(plist) == 1:
        line_color = (255, 255, 255)
        point = (x+(plist[0] % width)*scale, y+(plist[0]//width)*scale)
        pygame.draw.circle(window, line_color, point, 2)
        return

    segments = point_list_to_segments(plist)
    if use_color:
        colors = color_list(len(segments))
    else:
        colors = [(255, 255, 255)] * len(segments)
    for ix, seg in enumerate(segments):
        startp, endp = seg
        a = (x+(startp % width)*scale, y+(startp//width)*scale)
        b = (x+(endp % width)*scale, y+(endp//width)*scale)
        pygame.draw.lines(window, colors[ix], False, [a, b], 2)


def block_draw(window, plist, x: int , y: int, width: int, scale: int):
    ''' Draw a symbol by connecting the list of nodes in order.'''
    drawlist = []
    while len(plist) > 0:
        point = plist.pop()
        point = (int((x+(point % width)*scale)), int(y+(point // width)*scale))
        drawlist.append(point)

    # add lines to be drawn when flip() is called
    line_color = (255, 255, 255)  # white
    if len(drawlist) == 1:
        pygame.draw.circle(window, line_color, drawlist[0], 2)
    elif len(drawlist) > 1:
        pygame.draw.lines(window, line_color, False, drawlist, 2)
    else:
        print("Drawlist was empty for {},{}".format(x, y))


def calculate_neighbors(width, i, j):
    k = i * width + j  # node number
    neighbors = []
    for u in [-1, 0, 1]:
        if (i+u) >= 0 and (i+u) < width:
            for v in [-1, 0, 1]:
                if (j+v) >= 0 and (j+v) < width:
                    neigh = (i+u)*width + j+v
                    if neigh != k:  # self is not a neighbor
                        neighbors.append(neigh)
    return neighbors


def assign_neighbors(width):
    ''' Generates the list of neighbors for each node.'''
    nodes = []
    for i in range(width):
        for j in range(width):
            nodes.append(calculate_neighbors(width, i, j))
    return nodes


def build_pattern(start_neigh, node_adj, nodelist, pattern):
    ''' Build a list of nodes to visit connected to the current node, until
        no more unvisited nodes are reachable.'''

    curr_list = start_neigh.copy()
    # randomize the neighbor to be visited from each node
    random.shuffle(curr_list)
    while len(curr_list) > 0:
        neigh = curr_list[-1]
        del curr_list[-1]
        if neigh in pattern or neigh not in nodelist:
            # skip if visited or not in rectangle
            pass
        else:
            pattern.append(neigh)
            curr_list = node_adj[neigh].copy()
            random.shuffle(curr_list)


def generate_symbol(node_adj, nodelist):
    ''' Uses a subset of the nodes to generate a smaller rectangular symbol. '''

    # randomize the starting point
    pattern = []
    first = random.choice(nodelist)
    pattern.append(first)

    build_pattern(node_adj[first], node_adj, nodelist, pattern)

    # try to fill in emptiness by moving the original start node to the end of
    # the list, and continuing to add
    pattern.reverse()
    build_pattern(node_adj[pattern[-1]], node_adj, nodelist, pattern)

    return pattern


def populate(node_adj, window, screen_size: int, width: int, scale: int, use_color):
    ''' Fills the entire window with evenly-spaced symbols.'''
    for x in range(scale, screen_size-2*scale, width*scale):
        for y in range(scale, screen_size-2*scale, width*scale):
            nodelist = list(range(width*width))
            sym = generate_symbol(node_adj, nodelist)
            if use_color:
                rainbow_block_draw(window, sym, x, y, width, scale)
            else:
                block_draw(window, sym, x, y, width, scale)


def regen(window, num_symbol, width, scale, use_color):
    bg_color = (0, 0, 0)  # black
    pygame.display.get_surface().fill(bg_color)
    nodes = assign_neighbors(width)
    populate(nodes, window, screen_size, width, scale, use_color)
    # draw all symbols at once
    pygame.display.flip()


if __name__ == '__main__':
    '''Draws a grid of symbols given number of symbols and number of points (N).
    '''
    parser = argparse.ArgumentParser(description='symbol generator')
    parser.add_argument('--colors', action='store_true', default=False,
                        help='show stroke order using colors')
    parser.add_argument('--width', action='store', type=int, default=3,
                        help='width of symbols')
    parser.add_argument('--scale', action='store', type=int, default=20,
                        help='space between points and padding around symbols, in pixels')
    parser.add_argument('--num-symbol', action='store', type=int, default=None,
                        dest='num_symbol',
                        help='number of symbols to generate (square)')

    args = parser.parse_args()

    scale = args.scale
    width = args.width
    use_color = args.colors

    if args.num_symbol:
        num_symbol = args.num_symbol
    else:
        num_symbol = 700 // ((width - 1) * scale)  # default if no num_sym is provided

    # create the screen
    screen_size = (width * num_symbol + 1) * scale
    window = pygame.display.set_mode((screen_size, screen_size))
    regen(window, num_symbol, width, scale, use_color)

    # keep window open
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                regen(window, num_symbol, width, scale, use_color)
