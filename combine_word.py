def can_combine(first, second):
    if first == () or second == ():
        return True
    return first[-1] == second[0]


def check_can_combine(first, second, expected):
    if can_combine(first, second) == expected:
        print('PASS')
    else:
        print('FAIL', first, second)


def test_can_combine():
    check_can_combine(('', '', ''), ('', '', ''), True)
    check_can_combine(('a', 'd', ''), ('', 'c', 'b'), True)
    check_can_combine(('a', 'd', ''), ('e', 'c', 'b'), False)
    check_can_combine(('a', 'b'), tuple('b'), True)
    check_can_combine(('a', 'b'), ('c', 'd'), False)
    check_can_combine(('a', 'bae'), ('ac', 'd'), False)


def add_sound_parts(base, parts):
    assert can_combine(base, parts)
    if len(parts) <= 1:
        return base
    return base + parts[1:]


def check_add_sound_parts(base, parts, expected):
    if add_sound_parts(base, parts) == expected:
        print('PASS')
    else:
        print('FAIL', base, parts, expected)


def test_add_sound_parts():
    check_add_sound_parts(tuple(''), tuple(''), tuple(''))
    check_add_sound_parts(('', ''), ('', ''), ('', '', ''))
    check_add_sound_parts(('a', ''), ('', ''), ('a', '', ''))
    check_add_sound_parts(('a', ''), ('', 'b'), ('a', '', 'b'))
    check_add_sound_parts(('a', 'b'), ('b', 'c'), ('a', 'b', 'c'))

if __name__ == '__main__':
    test_can_combine()
    test_add_sound_parts()