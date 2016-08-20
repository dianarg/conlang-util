# a method of generating "flavored" words: http://archives.conlang.info/jhu/suervhua/qaulkenvhuen.html
# create words that sound like a language by combining existing words of the language
# can also use this method for names!


from divide_word import divide_word
from combine_word import add_sound_parts
from random import randint
from collections import defaultdict

if __name__ == '__main__':
    # word list to 'inspire' new words
    # TODO: not the best list for this; some pieces have no overlaps
    lexicon = ["apple", "orange", "banana", "kiwifruit", "grape", "grapefruit", "melon", "watermelon", "strawberry",
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

    bits_by_vowel = defaultdict(list)
    for w in lexicon:
        word_pieces = divide_word(w)
        for wp in word_pieces:
            bits_by_vowel[wp[0]].append(wp)

    num_new_words = 10

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
        print(''.join(new_word))
