# File: pos_tagging.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis


# PART B: POS tagging

from statements import *

# The tagset we shall use is:
# P  A  Ns  Np  Is  Ip  Ts  Tp  BEs  BEp  DOs  DOp  AR  AND  WHO  WHICH  ?

# Tags for words playing a special role in the grammar:

function_words_tags = [('a','AR'), ('an','AR'), ('and','AND'),
     ('is','BEs'), ('are','BEp'), ('does','DOs'), ('do','DOp'),
     ('who','WHO'), ('which','WHICH'), ('Who','WHO'), ('Which','WHICH'), ('?','?')]
     # upper or lowercase tolerated at start of question.

function_words = [p[0] for p in function_words_tags]

def unchanging_plurals():
    singular = set()
    plural = set()
    both = set()
    with open("sentences.txt", "r") as f:
        for line in f:
            for word in line.split():
                if (word.split('|')[1] == 'NN'):
                    singular.add(word.split('|')[0])
                elif (word.split('|')[1] == 'NNS'):
                    plural.add(word.split('|')[0])
    for w in singular:
        if w in plural:
            both.add(w)
    return both

unchanging_plurals_list = unchanging_plurals()

def noun_stem (s):
    """extracts the stem from a plural noun, or returns empty string"""
    vowels = "aeiou"

    stem = ""

    # Checks if word is an unchanging plurals
    if s in unchanging_plurals_list:
        return s
    # Checks if prefix is "men"
    elif re.match("[a-z]+men$", s):
        stem = s[:-2] + "an"
    else:
        # Use the previous rules
        if re.match("[a-z]+ies$", s):
            if s == "unties":
                stem = "untie"
            elif len(s) == 4 and not s[0] in vowels:
                stem = s[:-1]
            else:
                stem = s[:-3] + 'y'
        # Checks words ending in "es"
        elif re.match("[a-z]+es$", s):
            if re.match("[a-z]+(o|x|ch|sh|ss|zz)es$", s):
                stem = s[:-2]
            elif re.match("[a-z]+[^(sxyz)]es$", s) and s[-4:-2] != 'ch' and s[-4:-2] != 'sh':
                stem = s[:-1]
            elif re.match("[a-z]+(s|z)es$", s) and s[-4:-1] != "sse" and s[-4:-1] != "zze":
                stem = s[:-1]
        # Checks words ending in "s"
        elif re.match("[a-z]+s$", s):
            if s == "has":
                stem = "have"
            elif s[-2] == 'y' and s[-3] in vowels:
                stem = s[:-1]
            elif re.match("[a-z]+[^(sxyz)]s$", s) and s[-4:-2] != 'ch' and s[-4:-2] != 'sh':
                stem = s[:-1]
        # if it doesn't end in "s"
        else:
            stem = ""

    return stem

def tag_word (lx,wd):
    """returns a list of all possible tags for wd relative to lx"""
    tags = []
    # Checks if the tag is in the given function tags
    for tag in function_words_tags:
        if tag[0] == wd:
            tags.append(tag[1])
    # get proper noun and adjective matches from the lexicon
    for tag in ['P', 'A']:
        if wd in lx.getAll(tag):
            tags.append(tag)
    # get transitive and intransivite verb matches from the lexicon and tag singular or plural
    for tag in ['I', 'T']:
        if (wd in lx.getAll(tag)):
            if verb_stem(wd) == "":
                tags.append(tag + 'p')
            else:
                tags.append(tag + 's')
        elif ((verb_stem(wd) in lx.getAll(tag))):
            tags.append(tag + 's')
    # get noun matches from the lexicon and tag singular or plural
    if (wd in lx.getAll('N')) or (noun_stem(wd) in lx.getAll('N')):
        if wd in unchanging_plurals_list:
            tags.append('Ns')
            tags.append('Np')
        elif noun_stem(wd) == "":
            tags.append('Ns')
        else:
            tags.append('Np')
    return tags

def tag_words (lx, wds):
    """returns a list of all possible taggings for a list of words"""
    if (wds == []):
        return [[]]
    else:
        tag_first = tag_word (lx, wds[0])
        tag_rest = tag_words (lx, wds[1:])
        return [[fst] + rst for fst in tag_first for rst in tag_rest]


# End of PART B.
