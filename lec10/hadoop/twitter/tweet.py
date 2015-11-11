#!/usr/bin/python

import cPickle as pickle
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.tokenize import word_tokenize
import sys

sys.stderr.write("Started mapper.\n");
presidential_c = ['Carson','Clinton','Sanders','Trump'] 

def word_feats(words):
    # Turn a string into a list of feature words
    return dict([(word, True) for word in words])

def main(argv):
    # Classifier trained with example from:
    # http://streamhacker.com/2010/05/10/text-classification-sentiment-analysis-naive-bayes-classifier/
    classifier = pickle.load(open("movclass.p", "r"))
    
    for line in sys.stdin:
        # split line into words and test with classifier
        cur_p_c = None
        for p_c in presidential_c:
            if p_c in line:
                cur_p_c = p_c
        tolk_posset = word_tokenize(line.rstrip())
        d = word_feats(tolk_posset)
        
        if cur_p_c != None:
            print '%s\t%s' % ('LongValueSum:' + cur_p_c + '-' + classifier.classify(d), '1')

if __name__ == "__main__":
    main(sys.argv)


