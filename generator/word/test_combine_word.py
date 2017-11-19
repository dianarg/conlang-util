from combine_word import can_combine, add_sound_parts


def check_can_combine(first, second):
    assert can_combine(first, second), "unable to combine %s and %s" % (first, second)


def check_cannot_combine(first, second):
    assert can_combine(first, second) == False, "should not be able to combine %s and %s" % (first, second)


def test_can_combine():
    check_can_combine(('', '', ''), ('', '', ''))
    check_can_combine(('a', 'd', ''), ('', 'c', 'b'))
    check_can_combine(('a', 'b'), tuple('b'))


def test_cannot_combine():
    check_cannot_combine(('a', 'd', ''), ('e', 'c', 'b'))
    check_cannot_combine(('a', 'b'), ('c', 'd'))
    check_cannot_combine(('a', 'bae'), ('ac', 'd'))


def check_add_sound_parts(base, parts, expected):
    assert add_sound_parts(base, parts) == expected, "expected %s from %s and %s" % (expected, base, parts)


def test_add_sound_parts():
    check_add_sound_parts(tuple(''), tuple(''), tuple(''))
    check_add_sound_parts(('', ''), ('', ''), ('', '', ''))
    check_add_sound_parts(('a', ''), ('', ''), ('a', '', ''))
    check_add_sound_parts(('a', ''), ('', 'b'), ('a', '', 'b'))
    check_add_sound_parts(('a', 'b'), ('b', 'c'), ('a', 'b', 'c'))


if __name__ == '__main__':
    test_can_combine()
    test_add_sound_parts()
