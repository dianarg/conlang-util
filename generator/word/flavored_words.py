#!/usr/bin/env python

# A method of generating "flavored" words: http://archives.conlang.info/jhu/suervhua/qaulkenvhuen.html
# Creates words that sound like a language by combining existing words of the language.
# We can also use this method for names.
#
# To use, provide a CSV file as the commandline argument to the script.

from random import randint
from collections import defaultdict
import sys
import csv


# results look better if we don't consider Y a vowel
vowels = 'aeiouAEIOU'


def divide_word(word):
    pieces = []
    bit = ['', '', '']
    letter = 0
    b = 0
    while letter < len(word):
        if word[letter] in vowels:
            if b == 1:
                b = 2
            bit[b] += word[letter]
        else:
            if b == 2:  # reading vowels but we saw a consonant, go to next piece
                pieces.append(tuple(bit))
                start = bit[2]
                bit = [start, '', '']
                bit[1] += word[letter]
            else:
                bit[1] += word[letter]
            b = 1
        letter += 1
    pieces.append(tuple(bit))
    return pieces


def can_combine(first, second):
    if first == () or second == ():
        return True
    return first[-1] == second[0]


def add_sound_parts(base, parts):
    assert can_combine(base, parts)
    if len(parts) <= 1:
        return base
    return base + parts[1:]


def generate_words(word_list, num_new_words):
    bits_by_vowel = defaultdict(list)
    for w in word_list:
        # ignore case
        w = w.lower()
        word_pieces = divide_word(w)
        for wp in word_pieces:
            bits_by_vowel[wp[0]].append(wp)

    words = []
    for i in range(num_new_words):
        s = randint(0, len(bits_by_vowel['']) - 1)
        current = bits_by_vowel[''][s]
        new_word = current
        ending = current[-1]
        while ending != '' and ending in bits_by_vowel:
            n = randint(0, len(bits_by_vowel[ending])-1)
            current = bits_by_vowel[ending][n]
            new_word = add_sound_parts(new_word, current)
            ending = current[-1]
        words.append(''.join(new_word))
    return words


if __name__ == '__main__':
    # word list to 'inspire' new words
    # TODO: not the best list for this; some pieces have no overlaps
    word_list = ["apple", "orange", "banana", "kiwifruit", "grape", "grapefruit", "melon", "watermelon", "strawberry",
                 "blueberry", "peach", "pear", "plum", "persimmon", "carrot", "onion", "tomato", "avocado", "leek",
                 "cilantro", "spinach", "lettuce", "kale", "cabbage", "corn", "wheat", "oat", "barley", "malt", "ginger",
                 "cinnamon", "pepper", "salt", "acorn", "bokchoy", "chard", "rice", "mushroom", "bamboo", "shallot",
                 "potato", "raspberry", "cranberry", "pumpkin", "squash", "zucchini", "artichoke", "bean", "beet",
                 "turnip", "broccoli", "sprout", "blackberry", "plantain", "caper", "cauliflower", "cantaloupe", "celery",
                 "chive", "collard", "cucumber", "daikon", "dill", "eggplant", "endive", "fennel", "dandelion", "guava",
                 "huckleberry", "garbanzo", "jicama", "lentil", "lychee", "macadamia", "mango", "mustard", "honeydew",
                 "nectarine", "papaya", "parsley", "parsnip", "peanut", "pecan", "pineapple", "pomegranate", "radish",
                 "rhubarb", "rutabaga", "saffron", "soybean", "basil", "truffle", "watercress", "yam", "juniper",
                 "coconut", "cherry", "asparagus", "arugula", "mint"]
    # makes words like:
    # mabbacalelonion
    # baffroy
    # palt
    # lycheet
    # maspamboom

    # if input is provided, assume csv
    if len(sys.argv) > 1:
        word_list = []
        filename = sys.argv[1]
        with open(filename) as infile:
            rdr = csv.reader(infile)
            for row in rdr:
                word_list += row

    words = generate_words(word_list, 10)
    print(words)
