## AzzieL3MTools
## parse.py
## Hillman
## Jun 2025

import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
from string import punctuation
import re

# turned the following off...could run it once a week or as needed to update
#nltk.download('punkt')

# import pymupdf


# This lib will contain a set of relatively simple parsing tools to be used by the rest of the application

## text to words using simple python
def parse_to_wordlist(ptext):
    wordlist = [line.strip() for line in ptext.strip().split('\n') if line.strip()]
    return wordlist

# parse to words via nltk
def parse_to_tokens(text):
    wordlist = word_tokenize(text)
    return wordlist

# get the number of tokes
def count_tokens(text):
    wordlist = word_tokenize(text)
    return len(wordlist)


## need to figure out a nice way to extract titles witout punctuation
def parse_to_sentences(textlist):
    sentlist = nltk.sent_tokenize(textlist)
    flist = []
    holdit = ""
    for i in sentlist:
        ival = i.strip()
        if len(ival) < 5:
            holdit = ival + " " 
        else:
            flist.append(holdit + ival)
            holdit = ""
    return flist


def parse_to_paragraphs(text):
    return text.split('\n\n')


def runsentparse(tdata):
    tdata = tdata.replace("\n"," ")
    tres = parse_to_sentences(tdata)
    tset = ""
    for i in tres:
        tset += i + "\n\n"
    return tset

def runsentparsetolist(tdata):
    tdata = tdata.replace("\n"," ")
    tres = parse_to_sentences(tdata)
    tset = []
    for i in tres:
        tset.append(i)
    return tset


