#!/usr/bin/python

import cPickle as pickle
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
import sys

sys.stderr.write("Started mapper.\n");
presi_candidate = ['Carson','Clinton','Sanders','Trump']

def word_feats(words):
    # Turn a string into a list of feature words
    return dict([(word, True) for word in words])

def main(argv):
    
    classifier = pickle.load(open("movclass.p", "r"))
    
    for line in sys.stdin:
        # split line into words and test with classifier
        for p in presi_candidate:
            if p in line:
                presi = p
                    break
        tolk_posset = word_tokenize(line.rstrip())
        d = word_feats(tolk_posset)
        print presi + "-" + classifier.classify(d) + ":" + "\t" + "1"

if __name__ == "__main__":
    main(sys.argv)


