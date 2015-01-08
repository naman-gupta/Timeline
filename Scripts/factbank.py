#!/usr/bin/env python

"""
A tool for working with the pragmatic extension of FactBank.
"""

__author__ = "Christopher Potts"
__copyright__ = "Copyright 2011, Christopher Potts"
__credits__ = []
__license__ = "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License: http://creativecommons.org/licenses/by-nc-sa/3.0/"
__version__ = "1.0"
__maintainer__ = "Christopher Potts"
__email__ = "See the author's website"

######################################################################

import sys
import csv
from operator import itemgetter
from nltk.tree import Tree
from nltk.stem import WordNetLemmatizer

######################################################################

class FactbankCorpusReader:
    def __init__(self, filename):
        """Build a new corpus reader from the source filename."""        
        self.filename = filename

    def train_events(self):
        """Returns the list of train events."""
        return self.events(train_test='train')

    def test_events(self):
        """Returns the list of test events."""
        return self.events(train_test='test')

    def events(self, train_test=None):
        """
        Build the list of events. Use train_test='train' to limit to
        the training set, train_test='test' to limit to the test set,
        and train_test=None (the default) for the full set of events.
        """
        csvreader = csv.reader(open(self.filename))
        header = csvreader.next()
        events = []
        for row in csvreader:            
            events.append(Event(row, header))
        if train_test:
            events = filter((lambda e : e.TrainTest == train_test.lower()), events)
        return events

######################################################################

class Event:
    def __init__(self, row, header):
        """
        Create a new event object.

        Arguments:
        row --- a row from the source CSV file
        header -- the header row from the CSV file (= ['File', 'sentId', 'Sentence', 'SentenceParse',
                                                       'eId', 'eiId', 'eText', 'Normalization',
                                                       'FactValues', 'PragValues', 'TrainTest'])
        """
        d = dict(zip(header, row))
        self.File = d['File']
        self.sentId = d['sentId']
        self.Sentence = d['Sentence']
        self.SentenceParse = Tree(d['SentenceParse'])
        self.eId = d['eId']
        self.eiId = d['eiId']
        self.eText = d['eText']
        self.Normalization = d['Normalization']
        self.FactValues = self.__process_factvalues(d['FactValues'])
        self.PragValues = self.__process_pragvalues(d['PragValues'])
        self.TrainTest = d['TrainTest']

    def majority_pragvalue(self):
        """
        Returns the majority pragmatic value and its count if there is
        one, else (None, None).  (Ties for the majority result in no
        majority.)
        """        
        pairs = sorted(self.PragValues.items(), key=itemgetter(1), reverse=True)
        maj, maj_val = pairs[0]
        # Check for a tie:
        if pairs[1][1] == maj_val:
            return (None, None)
        else:
            return (maj, maj_val)

    def pos(self, wn_lemmatize=False):
        """
        Return the set of (word, pos) pairs of SentenceParse.
        wn_lemmatize=True to use the WordNet lemmatizer (default: False).
        """
        p = self.SentenceParse.pos()
        if wn_lemmatize:
            p = map(self.__wn_lemmatize, p)
        return p

    def leaves(self, wn_lemmatize=False):
        """
        Return the set of leaves of SentenceParse.
        wn_lemmatize=True to use the WordNet lemmatizer (default: False).
        """
        p = self.pos(wn_lemmatize=wn_lemmatize)
        return [lem[0] for lem in p]

    ######################################################################
    ##### INTERNAL METHODS
        
    def __process_factvalues(self, fv_string):
        """
        Internal method for processing the FactValue string from the CSV file which
        has the format

         ATTRIBUTION_STRING1:tag1|ATTRIBUTION_STRING2:tag2|...
          
        Returns a dictionary mapping source strings to tags.
        """
        parts = fv_string.split('|')
        d = {}
        for prt in parts:
            key, val = prt.split(':')
            d[key] = val
        return d

    def __process_pragvalues(self, pv_string):
        """
        Internal method for processing the PragValue string from the CSV file, which
        has the format

         ct_plus:count1|ct_minus:count2|...
          
        Returns a dictionary mapping source strings to tags.
        """
        parts = pv_string.split('|')
        d = {}
        for prt in parts:
            key, val = prt.split(':')
            d[key] = int(val)
        return d

    def __treebank2wn_pos(self, lemma):
        """
        Internal method for turning a lemma's pos value into one that
        is compatible with WordNet, where possible (else the tag is
        left alone).
        """
        string, tag = lemma
        tag = tag.lower()
        if tag.startswith('v'):
            tag = 'v'
        elif tag.startswith('n'):
            tag = 'n'
        elif tag.startswith('j'):
            tag = 'a'
        elif tag.startswith('rb'):
            tag = 'r'
        return (string, tag)

    def __wn_lemmatize(self, lemma):
        """
        Lemmatize lemma using wordnet.stemWordNetLemmatizer(). Always
        returns a (string, pos) pair.  Lemmarizes even when the tag
        isn't helpful, by ignoring it for stemming.
        """
        string, tag = self.__treebank2wn_pos(lemma)
        wnl = WordNetLemmatizer()
        if tag in ('a', 'n', 'r', 'v'):
            string = wnl.lemmatize(string, tag)
        else:
            string = wnl.lemmatize(string)
        return (string, tag)

######################################################################

if __name__ == '__main__':
    fb = FactbankCorpusReader('fb-semprag.csv')
    for event in fb.iter_events(display_progress=False):
        if 'AUTHOR' in event.FactValues:        
            print event.majority_pragvalue(), event.FactValues['AUTHOR']
    

