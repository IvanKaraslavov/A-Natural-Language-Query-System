import pytest
from pos_tagging import (
    noun_stem,
    tag_word,
    tag_words,
)

# Short guide:
# pip install -U pytest

# Run $ pytest test_tagging.py::test_processing to run single testcase
# or  $ pytest to run them all.
from statements import Lexicon

noun2stem = {
    "sheep": "sheep",
    "women": "woman",
    "dogs": "dog",
    "oranges": "orange",
    "": "",
}

def test_tagging():
    failures = []
    for word, stem in noun2stem.items():
        stem_found = noun_stem(word)
        if not stem_found == stem:
            failures.append((stem, stem_found))
    assert failures == []


def test_function_words():
    cases = {
        'a': ['AR'],
        'an': ['AR'],
        'and': ['AND'],
        'is': ['BEs'],
        'are': ['BEp'],
        'does': ['DOs'],
        'do': ['DOp'],
        'who': ['WHO'],
        'which': ['WHICH'],
        'Who': ['WHO'],
        'Which': ['WHICH'],
        '?': ['?'],
    }

    l = Lexicon()
    for w, tags in cases.items():
        assert tag_word(l, w) == tags


def test_taging_with_trained_lexer():
    lx = Lexicon()
    lx.add("John", "P")
    lx.add("orange", "N")
    lx.add("orange", "A")
    lx.add("fish", "N")
    lx.add("fish", "I")
    lx.add("like", "T")

    word2tags = {
        "John": ["P"],
        "orange": ["A", "Ns"],
        "fish": ['Ip', 'Np', 'Ns'],
        "a": ["AR"],
        "zxghqw": [],
        "likes": ["Ts"],
    }

    for w, tags in word2tags.items():
        assert sorted(tag_word(lx, w)) == tags


    # tag_combinations = tag_words(lx, word2tags.keys())
    # for tags in word2tags.values():
    #     assert tags in tag_combinations

def test_tag_words():
    lx = Lexicon()

    assert tag_words(lx, ['a']) == [['AR']]
    assert tag_words(lx, ['and']) == [['AND']]
    assert tag_words(lx, ['a', 'and']) == [['AR', 'AND']]

    assert tag_words(lx, ['a', 'and', 'does']) == [
        ['AR', 'AND', 'DOs']
    ]