#!/usr/bin/env python

import sys
import random

from simple_gen import gen_name


# TODO: doesn't really need a self because there are a fixed number of these
class Biome:
    biomes = ['forest', 'plains', 'ocean', 'desert', 'tundra']

    @staticmethod
    def make_random():
        return Biome(random.choice(Biome.biomes))

    def __init__(self, n):
        self.name = n

    def __repr__(self):
        visual = {
            'forest': '^',
            'plains': ',',
            'ocean':  '~',
            'desert': '.',
            'tundra': '*',
        }
        return visual[self.name]


class Landmark:
    shapes = ['&', 'W', '@']

    def __init__(self):
        self.name = gen_name()
        self.shape = random.choice(Landmark.shapes)

    def __repr__(self):
        return ' _{s}_ {n}'.format(s=self.shape, n=self.name)


class Religion:
    def __init__(self):
        self.name = gen_name()
        self.gods = []

    def __repr__(self):
        return '{n} ({g})'.format(n=self.name, g=', '.join(self.gods))

    def add_god(self, name):
        self.gods.append(name)

class Land:
    def __init__(self):
        self.name = gen_name()
        self.biome = Biome.make_random()
        self.landmark = []
        self.pop = 0
        self.religion = None

    def __repr__(self):
        name = self.name
        pop_string = 'pop: {}'.format(self.pop)
        rel_string = 'rel: {}'.format(self.religion if self.religion else '')
        max_width = max([len(name), len(pop_string), len(rel_string)])
        for mark in self.landmark:
            if max_width < len(str(mark)):
                max_width = len(str(mark))
        if len(name) < max_width:
            name += ' '*(max_width - len(name))
        if len(pop_string) < max_width:
            pop_string += ' '*(max_width - len(pop_string))
        if len(rel_string) < max_width:
            rel_string += ' '*(max_width - len(rel_string))

        frame_width = max_width + 4
        s = frame_width*'{c}' + '\n'
        s += '{c} {name} {c}\n'
        for mark in self.landmark:
            s += '{c} {mark} {c}\n'.format(mark=mark, c=self.biome)
        s += '{c} {pop} {c}\n'
        s += '{c} {religion} {c}\n'
        s += frame_width*'{c}' + '\n'
        return s.format(c=self.biome, name=name, pop=pop_string, religion=rel_string)

    def update(self):
        roll = random.randint(1, 10)
        if roll == 1:
            rel = Religion()
            print('people are now following {}'.format(rel.name))
            self.religion = rel
        elif roll == 2:
            print('plague!')
            self.pop /= 2
        elif roll == 3:
            mark = Landmark()
            print('a natural disaster created a landmark: {}'.format(mark))
            self.landmark.append(mark)
        elif roll == 4 and len(self.landmark) > 1 and self.religion:
            mark = random.choice(self.landmark)
            print('followers of {rel} erected a religious site at {mark}'.format(rel=self.religion, mark=mark))
            if len(self.religion.gods) > 1:
                god = random.choice(self.religion.gods)
                # TODO: update mark
                print('it is dedicated to {}'.format(god))
            # todo: update landmark with religious site  |M|  /|.U.|\
        elif roll == 5 and self.religion:
            god = gen_name()
            print('followers of {rel} have started to worship {god}'.format(rel=self.religion, god=god))
            self.religion.add_god(god)
        elif roll == 6 and len(self.landmark) > 1:
            # TODO religious offerings if a site is dedicated to a god
            pass
        else:
            self.pop += 1

def main():
    land = Land()
    num_ticks = 20
    for tick in range(num_ticks):
        print('tick {}'.format(tick))

        land.update()

        print(land)
        print()

if __name__ == '__main__':
    main()
