import sys
import random
# import and init pygame
import pygame
pygame.init()

'''
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

# constants
white = (255, 255, 255)
black = (0, 0, 0)

bg_color = black
line_color = white
n = 3  # size of symbols
scale = 10  # distance between nodes within symbol and between symbols


def block_draw(plist, x, y):
    ''' Draw a symbol by connecting the list of nodes in order.'''
    drawlist = []
    while len(plist) > 0:
        point = plist.pop()
        drawlist.append((x+(point % n)*scale, y+(point/n)*scale))

    # add lines to be drawn when flip() is called
    pygame.draw.lines(window, line_color, False, drawlist, 2)


def calculate_neighbors(i, j):
    k = i*n + j  # node number
    neighbors = []
    for u in [-1, 0, 1]:
        if (i+u) >= 0 and (i+u) < n:
            for v in [-1, 0, 1]:
                if (j+v) >= 0 and (j+v) < n:
                    neigh = (i+u)*n + j+v
                    if neigh != k:  # self is not a neighbor
                        neighbors.append(neigh)
    return neighbors


def assign_neighbors():
    ''' Generates the list of neighbors for each node.'''
    nodes = []
    for i in range(n):
        for j in range(n):
            # nodes.append([])
            nodes.append(calculate_neighbors(i, j))
    return nodes


def build_pattern(start_neigh, nodes, pattern):
    ''' Build a list of nodes to visit connected to the current node, until
        no more unvisited nodes are reachable.'''
    num = 0
    while len(start_neigh) > num:
        if start_neigh[num] in pattern:
            # skip if visited
            num += 1
        else:
            pattern.append(start_neigh[num])
            start_neigh = nodes[start_neigh[num]]
            num = 0


def generate_symbol(nodes):
    # randomize the neighbor to be visited from each node
    for nd in nodes:
        random.shuffle(nd)

    # randomize the starting point
    pattern = []
    first = random.randint(0, n*n-1)
    pattern.append(first)

    build_pattern(nodes[first], nodes, pattern)

    # try to fill in emptiness by moving the original start node to the end of
    # the list, and continuing to add
    pattern.reverse()
    build_pattern(nodes[pattern[-1]], nodes, pattern)

    return pattern


def populate():
    ''' Fills the entire window with evenly-spaced symbols.'''
    nodes = assign_neighbors()
    for x in range(scale, screen_size-2*scale, n*scale):
        for y in range(scale, screen_size-2*scale, n*scale):
            sym = generate_symbol(nodes)
            block_draw(sym, x, y)


# create the screen
num_sym = 700/((n-1)*scale)
screen_size = scale + (n)*scale*num_sym + scale
window = pygame.display.set_mode((screen_size, screen_size))
pygame.display.get_surface().fill(bg_color)

populate()

# draw all symbols at once
pygame.display.flip()

# keep window open
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            pass