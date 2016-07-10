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


# TODO: install pytest
def check_divide_word(word, expected):
    pieces = divide_word(word)
    if pieces == expected:
        print('PASS')
    else:
        print('FAIL', word, expected, pieces)


def test_divide_word():
    check_divide_word('', [('', '', '')])
    check_divide_word('a', [('a', '', '')])
    check_divide_word('ai', [('ai', '', '')])
    check_divide_word('x', [('', 'x', '')])
    check_divide_word('xx', [('', 'xx', '')])
    check_divide_word('ax', [('a', 'x', '')])
    check_divide_word('xa', [('', 'x', 'a')])
    check_divide_word('axe', [('a', 'x', 'e')])
    check_divide_word('xxa', [('', 'xx', 'a')])
    check_divide_word('xax', [('', 'x', 'a'), ('a', 'x', '')])
    check_divide_word('axaxa', [('a', 'x', 'a'), ('a', 'x', 'a')])

    check_divide_word('miniature', [('', 'm', 'i'), ('i', 'n', 'ia'), ('ia', 't', 'u'), ('u', 'r', 'e')])
    check_divide_word('school', [('', 'sch', 'oo'), ('oo', 'l', '')])
    check_divide_word('alleviate', [('a', 'll', 'e'), ('e', 'v', 'ia'), ('ia', 't', 'e')])

if __name__ == '__main__':
    test_divide_word()
