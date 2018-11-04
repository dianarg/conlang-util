# placeholder generator functions for civisim

import random

def gen_name(num_names=1):
    vowels = 'aeiou'
    consonants = 'qwrtypsdfghjklzxcvbnm'
    names = []
    for _ in range(num_names):
        num_let = random.randint(3, 7)
        name = ''
        vowel = False
        for _ in range(num_let):
            if vowel:
                name += random.choice(vowels)
            else:
                name += random.choice(consonants)
            vowel = not vowel
        names.append(name.title())
    return ' '.join(names)

# todo: generate these gen functions
def gen_died():
    verbs = ['died', 'retired', 'abdicated']
    return random.choice(verbs)


def gen_reason():
    reasons = ['after being poisoned', 'with sword in hand', 'because of old age', 'after defeat in battle']
    return random.choice(reasons)


def gen_tribe_type():
    types = ['tribe', 'kingdom', 'nation']
    return random.choice(types)


def gen_item():
    items = ['a black ram', 'food', 'noble blood', 'jewels']
    return random.choice(items)


def gen_leader_trait():
    traits = ['proud', 'strong', 'fair', 'just', 'ruthless', 'capable', 'lazy', 'tyrannical']
    return random.choice(traits)


def gen_title():
    titles = ['King', 'Queen', 'Chief', 'High Priest', 'High Priestess', 'Duke', 'Emperor', 'Empress', 'Admiral', 'General', 'Warchief']
    return random.choice(titles)


def gen_item_desc():
    desc = [
        'It gleams brilliant in the moonlight.',
        'It shines brightly in the midday sun.',
    ]
    return random.choice(desc)


def gen_temple_desc():
    desc = [
        'It is a circle of standing stones aligned to the movement of the heavens.',
        'It is an earthen mound.',
        'The monument is a stone pyramid.',
        'It is marble tower with frightening statues adorning the walls.',
        'The temple of limestone and alabaster contains many splendid rooms.',
    ]
    return random.choice(desc)


def gen_biome():
    biome = ['chaparral', 'temperate forest', 'savanna', 'tropical rainforest', 'tropical desert',
             'cold desert', 'tundra', 'ocean', 'flood plain']
    return random.choice(biome)


def generator(base):
    funs = {
        'name': gen_name,
        'gov': gen_name,
        'died': gen_died,
        'reason': gen_reason,
        'landmark': gen_name,
        'site_name': gen_name,
        'region': gen_name,
        'site': gen_name,
        'god': gen_name,
        'tribe_type': gen_tribe_type,
        'region': gen_name,
        'item': gen_item,
        'title': gen_title,
        'leader_trait': gen_leader_trait,
        'city': gen_name,
        'item_desc': gen_item_desc,
        'temple_desc': gen_temple_desc,
    }
    rv = 'DEFAULT_' + base
    if base in funs:
        rv = funs[base]()
    return rv
