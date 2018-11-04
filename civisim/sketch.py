#!/usr/bin/env python

import random
import sys

from simple_gen import generator, gen_name, gen_biome


# attributes of a civ
class Civ:
    # traits
    # attitute toward other civ
    # list of culture
    # list of languages
    pass


# alternative
class Language:
    # called by culture, religion
    def add_word():
        pass
    pass


class Religion:
    # preferred language
    def __init__(self):
        self.founder = gen_name(num_names=1)
        self.name
        self.gods = []


class Culture:
    # preferred language
    pass


class Military:
    # A violent organization that exerts control by force.  includes pirate/bandit gangs, army, police force.
    pass


class Government:
    # includes military? or separate civilian govt?
    # city-state gov for single city.  can evolve into empire
    # could also be religious
    pass


# todo: update to also parse # fields in string
def parse_field(field):
    rv = ''
    at = ''
    st = 'start'
    for c in field:
        if c == '#':
            st = 'attrs'
        elif st == 'start' and c not in '0123456789':
            rv += c
        elif st == 'attrs':
            at += c
    return rv, at


def parse_event(ev_fmt):
    num = len(ev_fmt)
    vars = {}
    st = 'open'
    curr_v = ''
    for c in ev_fmt:
        if st == 'open' and c == '{':
            st = 'word'
        elif st == 'word' and c != '}':
            curr_v += c
        elif st == 'word' and c == '}':
            if curr_v not in vars:
                base, attrs = parse_field(curr_v)
                gen = generator(base)
                # todo: add function to handle attrs
                if 'pl' in attrs:
                    gen += 's'
                vars[curr_v] = gen
            curr_v = ''
            st = 'open'
    return vars


def gen_event(region):
    events = ["{name1} of {gov1} marries {name2} of {gov2}, cementing an alliance between the two {tribe_type#pl}.",
              "{name1}, {title} of {gov}, has {died} {reason}.  {title} {name2} has risen, promising to be a {leader_trait} leader.",
              "A new city called {city} is flourishing in {region}.  The government is {gov}.",
              "A new religious site called {site} has been erected at {landmark}.  {temple_desc}",
              "The people of {region} make an offering of {item} to their god {god} at {site}. {item_desc}",
    ]
    ev_fmt = random.choice(events)
    vars = parse_event(ev_fmt)
    vars['region'] = region

    return ev_fmt.format(**vars)

# TODO: more events
# civil war, revolution, rebellion: one civ splits into two
# religion split: reformation
# prophet: new religion



# attributes of a world hex
class Land:
    # total population
    # percent language
    # percent culture
    # percent religion
    # military control (level, civ)
    # government control (level, civ)
    # diplomatic claims

    def __repr__(self):
        return ""

    def __init__(self):
        self.name = gen_name()
        self.biome = gen_biome()
        self.religion = 'R'
        self.civ = 'C'


# TODO: class
def draw_grid(grid):
    for row in grid:
        for cell in row:
            sys.stdout.write('{} \t'.format(cell.name))
        sys.stdout.write('\n')
        for cell in row:
            sys.stdout.write('{} \t'.format(cell.biome))
        sys.stdout.write('\n')
        for cell in row:
            sys.stdout.write('R: {} \t'.format(cell.religion))
        sys.stdout.write('\n\n')


# TODO: have events be generated for a given region based on what is present in that region
# religion in the region is prereq for new religion site
# religious site is prereq for offering
# gov is prereq for leader change




def main():

    num_ticks = 2
    num_civs = 5
    num_religions = 5
    grid_size = 4
    grid = []
    regions = {}
    status = {'civs': [], 'religions': [], 'govs': [], 'lands': []}
    # set of starting civs
    for _ in range(num_civs):
        status['civs'].append(gen_name())
    for _ in range(num_religions):
        status['religions'].append(gen_name())
    for row in range(grid_size):
        grid.append([])
        for col in range(grid_size):
            grid[row].append(Land())
            new_reg = grid[row][col]
            # cache to easily look up regions
            regions[new_reg.name] = new_reg
    print(regions)

    # run world ticks
    for tick in range(num_ticks):
        # make dates
        sys.stdout.write('It is the tick {} C.E.\n'.format(tick))

        draw_grid(grid)

        # god events

        # random events
        region_name = random.choice(list(regions.keys()))
        event = gen_event(region_name)
        sys.stdout.write('{}\n'.format(event))
        # update terrain

        # update population

        # update culture

        # update political claims

        # print status
        sys.stdout.write('\n{}\n'.format(status))


if __name__ == '__main__':
    main()
