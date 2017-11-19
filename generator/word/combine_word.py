def can_combine(first, second):
    if first == () or second == ():
        return True
    return first[-1] == second[0]


def add_sound_parts(base, parts):
    assert can_combine(base, parts)
    if len(parts) <= 1:
        return base
    return base + parts[1:]

