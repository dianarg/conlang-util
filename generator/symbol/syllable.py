#!/usr/bin/env python

import sys
import argparse
import random
import pygame
import symbolgen

'''
Use symbolgen with rectangular blocks to make syllable glyphs.
'''


def make_blocks(width):
    '''
    Make two cuts, random location and direction.  Second cut may stop
    when it encounters the first.

    n = 5
    cut0 = 1, vertical
    cut1 = 1, horizontal
    0 1 2 3 4      0 1   2 3 4
    5 6 7 8 9      5 6   7 8 9
    a b c d e  ->  a b          c d e
    f g h i j      f g          h i j
    k l m n o      k l          m n o

    '''
    result = []
    is_vert = random.choice([True, False])
    cut0 = random.randint(0, width)
    cut1 = random.randint(0, width)

    # first cut
    side0 = []
    side1 = []
    if not is_vert:
        nodes = list(range(width*width))
        mid = (cut0+1)*width
        side0 = nodes[:mid]
        side1 = nodes[mid:]
    else:
        for x in range(width):
            for y in range(width):
                k = x * width + y  # node number
                if y <= cut0:
                    side0.append(k)
                else:
                    side1.append(k)

    is_vert = not is_vert
    cut_side0 = random.choice([True, False])
    cut_side1 = random.choice([True, False])

    # second cut
    for do_cut, side in zip([cut_side0, cut_side1], [side0, side1]):
        if not do_cut:
            result.append(side)
        else:
            sub0 = []
            sub1 = []
            for nn in side:
                x = nn // width
                y = nn % width
                if not is_vert and x <= cut1:
                    sub0.append(nn)
                elif not is_vert:
                    sub1.append(nn)
                elif y <= cut1:
                    sub0.append(nn)
                else:
                    sub1.append(nn)
            result.append(sub0.copy())
            result.append(sub1.copy())
    return result


def populate(node_adj, window, screen_size: int, width: int, scale: int, use_color):
    ''' Fills the entire window with evenly-spaced symbols.'''
    for x in range(scale, screen_size-2*scale, width*scale):
        for y in range(scale, screen_size-2*scale, width*scale):
            blocks = make_blocks(width)
            for nodelist in blocks:
                if len(nodelist) > 0:
                    sym = symbolgen.generate_symbol(node_adj, nodelist)
                    if use_color:
                        symbolgen.rainbow_block_draw(window, sym, x, y, width, scale)
                    else:
                        symbolgen.block_draw(window, sym, x, y, width, scale)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='syllable generator')
    parser.add_argument('--colors', action='store_true', default=False,
                        help='show stroke order using colors')
    parser.add_argument('--width', action='store', type=int, default=3,
                        help='width of symbols')
    parser.add_argument('--scale', action='store', type=int, default=30,
                        help='space between points and padding around symbols, in pixels')
    parser.add_argument('--num-symbol', action='store', type=int, default=6,
                        dest='num_symbol',
                        help='number of symbols to generate (square)')

    args = parser.parse_args()
    num_symbol = args.num_symbol
    width = args.width
    scale = args.scale
    use_color = args.colors

    # create the screen
    screen_size = (width * num_symbol + 1) * scale
    window = pygame.display.set_mode((screen_size, screen_size))
    bg_color = (0, 0, 0)  # black
    pygame.display.get_surface().fill(bg_color)

    # define node adjacency
    node_adj = symbolgen.assign_neighbors(width)

    # generate random symbols
    populate(node_adj, window, screen_size, width, scale, use_color)

    # draw all symbols at once
    pygame.display.flip()

    # keep window open
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN:
                pass
