from correction import replace_u, restore_u, correction, candidates

def spell_check(word):
    word = replace_u(word.lower())
    corrected_word = max(candidates(word), key = correction.P)
    return restore_u(corrected_word)
