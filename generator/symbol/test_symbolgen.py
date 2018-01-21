from symbolgen import point_list_to_segments, calculate_neighbors, num_to_symbol


def check_point_list_to_segments(points, expected):
    assert point_list_to_segments(points) == expected


def check_calculate_neighbors(n, x, y, expected):
    assert n >= 2
    assert calculate_neighbors(n, x, y) == expected


def check_num_to_symbol(width, num_str, symbol):
    assert num_to_symbol(width, num_str) == symbol


def check_num_to_symbol_error(width, num_str, error_str='invalid literal'):
    try:
        num_to_symbol(width, num_str)
    except ValueError as ex:
        assert error_str in str(ex)
    else:
        assert False, 'expect invalid input error for: ' + num_str


def test_point_list_to_segments():
    check_point_list_to_segments([1], [])
    check_point_list_to_segments([1, 2],
                                 [(1, 2)])
    check_point_list_to_segments([1, 3, 2],
                                 [(1, 3), (3, 2)])
    check_point_list_to_segments([1, 3, 2, 4, 6, 5],
                                 [(1, 3), (3, 2), (2, 4), (4, 6), (6, 5)])


def test_calculate_neighbors():
    n = 2
    '''
    0 1
    2 3
    '''
    check_calculate_neighbors(n, 0, 0, [1, 2, 3])
    check_calculate_neighbors(n, 0, 1, [0, 2, 3])
    check_calculate_neighbors(n, 1, 0, [0, 1, 3])
    check_calculate_neighbors(n, 1, 1, [0, 1, 2])

    n = 3
    '''
    0 1 2
    3 4 5
    6 7 8
    '''
    check_calculate_neighbors(n, 0, 0, [1, 3, 4])
    check_calculate_neighbors(n, 0, 1, [0, 2, 3, 4, 5])
    check_calculate_neighbors(n, 0, 2, [1, 4, 5])
    check_calculate_neighbors(n, 1, 0, [0, 1, 4, 6, 7])
    check_calculate_neighbors(n, 1, 1, [0, 1, 2, 3, 5, 6, 7, 8])
    check_calculate_neighbors(n, 1, 2, [1, 2, 4, 7, 8])
    check_calculate_neighbors(n, 2, 0, [3, 4, 7])
    check_calculate_neighbors(n, 2, 1, [3, 4, 5, 6, 8])
    check_calculate_neighbors(n, 2, 2, [4, 5, 7])


def test_num_to_symbol():
    check_num_to_symbol(3, '', [])
    check_num_to_symbol(3, '2', [2])
    check_num_to_symbol(3, '12567', [1, 2, 5, 6, 7])
    check_num_to_symbol(6, '9abnz', [9, 10, 11, 23, 35])

    check_num_to_symbol_error(2, '4')
    check_num_to_symbol_error(3, 'a')
    check_num_to_symbol_error(4, 'g')
    check_num_to_symbol_error(5, 'p')
    check_num_to_symbol_error(6, '%')
    check_num_to_symbol_error(7, '0', 'integer base')
