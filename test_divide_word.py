from divide_word import divide_word


def check_divide_word(word, expected):
    pieces = divide_word(word)
    assert pieces == expected, "divide_word(%s) produced %s, expected %s" % (word, pieces, expected)


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
