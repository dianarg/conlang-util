# a method of generating "flavored" words: http://archives.conlang.info/jhu/suervhua/qaulkenvhuen.html
# can also use this method for names!

from divide_word import *
from random import randint


def can_combine(first, second):
    return first[2] == second[0]


def check_can_combine(first, second, expected):
    if can_combine(first, second) == expected:
        print 'PASS'
    else:
        print 'FAIL', first, second


def test_can_combine():
    check_can_combine(('', '', ''), ('', '', ''), True)
    check_can_combine(('a', 'd', ''), ('', 'c', 'b'), True)
    check_can_combine(('a', 'd', ''), ('e', 'c', 'b'), False)


def add_sound_parts(base, parts):
    return base + ''.join(parts)


def check_add_sound_parts(base, parts, expected):
    if add_sound_parts(base, parts) == expected:
        print 'PASS'
    else:
        print 'FAIL', '"'+base+'"', parts, '"'+expected+'"'


def test_add_sound_parts():
    check_add_sound_parts('', ('', '', ''), '')
    check_add_sound_parts('', ('a', '', ''), 'a')
    check_add_sound_parts('a', ('', '', ''), 'a')
    check_add_sound_parts('a', ('a', '', ''), 'aa')
    check_add_sound_parts('a', ('b', 'cc', 'd'), 'abccd')

if __name__ == '__main__':
    test_can_combine()
    test_add_sound_parts()
