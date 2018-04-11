import re
import pickle
from collections import Counter


letters = ['ա', 'բ', 'գ', 'դ', 'ե', 'զ', 'է', 'ը', 'թ', 'ժ', 'ի', 'լ',\
           'խ','ծ','կ','հ','ձ','ղ','ճ', 'մ','յ','ն','շ','ո','չ',\
           'պ','ջ', 'ռ','ս','վ','տ','ր','ց','u', 'փ','ք','և','օ','ֆ']


pkl_file = open('filtered_words.pkl', 'rb')
filtered_words = pickle.load(pkl_file)
pkl_file.close()


def replace_u(word):
    while 'ու' in word:
        index = word.index('ու')
        word = word[:index] + 'u' + word[index + 2:]
    return word

def restore_u(word):
    while 'u' in word:
        index = word.index('u')
        word = word[:index] + 'ու' + word[index + 1:]
    return word

def is_word(word):
    for i in word:
        if i not in letters:
            return False
    return True


WORDS = Counter()
for i in filtered_words.keys():
    newword = replace_u(i)
    if is_word(newword):
        WORDS[newword] = filtered_words[i]

N = sum(WORDS.values())


def words(text):
    return re.findall(r'\w+', text.lower())

def P(word):
    return WORDS[word] / N

def known(words):
    return set(w for w in words if w in WORDS)

def candidates(word):
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def edits1(word):
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    return set(ed2 for ed1 in edits1(word) for ed2 in edits1(ed1))
