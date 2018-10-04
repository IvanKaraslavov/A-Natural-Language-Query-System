# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis
# Revised October 2017 by Chunchuan Lyu


# PART A: Processing statements


def add(lst, item):
    if (item not in lst):
        lst.insert(len(lst), item)


class Lexicon:
    """stores known word stems of various part-of-speech categories"""
    def __init__(self):
        self.wordsMap = []

    def add(self, stem, cat):
        self.wordsMap.append((stem, cat))

    def getAll(self, cat):
        return [tuple[0] for tuple in set(self.wordsMap) if tuple[1] == cat]


class FactBase:
    """stores unary and binary relational facts"""
    def __init__(self):
        self.unaryList = []
        self.binaryList = []

    def addUnary(self, pred, e1):
        self.unaryList.append((pred, e1))

    def addBinary(self, pred, e1, e2):
        self.binaryList.append((pred, e1, e2))

    def queryUnary(self, pred, e1):
        return (pred, e1) in self.unaryList

    def queryBinary(self, pred, e1, e2):
        return (pred, e1, e2) in self.binaryList


import re
from nltk.corpus import brown

verb_cache = {}
vb_list = [word for (word, tag) in set(brown.tagged_words()) if tag == "VB"]
vbz_list = [word for (word, tag) in set(brown.tagged_words()) if tag == "VBZ"]
def verb_stem(s):
    """extracts the stem from the 3sg form of a verb, or returns empty string"""

    vowels = "aeiou"
    stem = ""
    for cache_word, cache_stem in verb_cache.items():
        if(s == cache_word):
            return cache_stem

    # Checks words ending in "ies"
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
        else:
            verb_cache[s] = ""
            return ""
    # Checks words ending in "s"
    elif re.match("[a-z]+s$", s):
        if s == "has":
            return "have"
        elif s[-2] == 'y' and s[-3] in vowels:
            stem = s[:-1]
        elif re.match("[a-z]+[^(sxyz)]s$", s) and s[-4:-2] != 'ch' and s[-4:-2] != 'sh':
            stem = s[:-1]
        else:
            verb_cache[s] = ""
            return ""
    # if it doesn't end in "s"
    else:
        verb_cache[s] = ""
        return ""
    # Checks if the stem has a tag "VB" or the word has a tag "VBZ" in the brown corpus
    if not (stem in set(vb_list) or s in set(vbz_list)):
        verb_cache[s] = ""
        return ""
    else:
        verb_cache[s] = stem
        return stem




def add_proper_name(w, lx):
    """adds a name to a lexicon, checking if first letter is uppercase"""
    if ('A' <= w[0] and w[0] <= 'Z'):
        lx.add(w, 'P')
        return ''
    else:
        return (w + " isn't a proper name")


def process_statement(lx, wlist, fb):
    """analyses a statement and updates lexicon and fact base accordingly;
       returns '' if successful, or error message if not."""
    # Grammar for the statement language is:
    #   S  -> P is AR Ns | P is A | P Is | P Ts P
    #   AR -> a | an
    # We parse this in an ad hoc way.
    msg = add_proper_name(wlist[0], lx)
    if (msg == ''):
        if (wlist[1] == 'is'):
            if (wlist[2] in ['a', 'an']):
                lx.add(wlist[3], 'N')
                fb.addUnary('N_' + wlist[3], wlist[0])
            else:
                lx.add(wlist[2], 'A')
                fb.addUnary('A_' + wlist[2], wlist[0])
        else:
            stem = verb_stem(wlist[1])
            if (len(wlist) == 2):
                lx.add(stem, 'I')
                fb.addUnary('I_' + stem, wlist[0])
            else:
                msg = add_proper_name(wlist[2], lx)
                if (msg == ''):
                    lx.add(stem, 'T')
                    fb.addBinary('T_' + stem, wlist[0], wlist[2])
    return msg

# End of PART A.
