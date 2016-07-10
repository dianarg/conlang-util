# a method of generating "flavored" words: http://archives.conlang.info/jhu/suervhua/qaulkenvhuen.html
# create words that sound like a language by combining existing words of the language
# can also use this method for names!


from divide_word import *
from combine_word import *
from random import randint


if __name__ == '__main__':
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

    processed_words = {w: divide_word(w) for w in lexicon}

    # TODO: dict of pieces grouped by starting vowel

    num_new_words = 10

    for i in range(num_new_words):
        s = randint(0, len(lexicon) - 1)
        start = processed_words[lexicon[s]]
        new_word = start[0]
        current_piece = start[0]  # first piece in word
        n1 = randint(0, len(lexicon) - 1)
        n2 = (n1 - 1) % len(lexicon)
        while n1 != n2:
            next_word = processed_words[lexicon[n1]]
            i = 0
            while i < len(next_word) and not can_combine(current_piece, next_word[i]):
                i += 1
            if i < len(next_word):
                current_piece = next_word[i]
                new_word = add_sound_parts(new_word, current_piece)
                if current_piece[-1] != '':
                    n1 = randint(0, len(lexicon) - 1)
                    n2 = (n1 - 1) % len(lexicon)
                else:
                    break
            else:
                n1 = (n1 + 1) % len(lexicon)

        print(''.join(new_word))


#examples:
#neggplamorarleydennefruit
#plucentiper
#porabbappleler
#bacon
#jilard
#lerrycheet