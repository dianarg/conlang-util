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

