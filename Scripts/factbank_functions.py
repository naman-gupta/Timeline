#!/usr/bin/env python

"""A few simple examples of factbank.py functions."""

__author__ = "Christopher Potts"
__copyright__ = "Copyright 2011, Christopher Potts"
__credits__ = []
__license__ = "Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License: http://creativecommons.org/licenses/by-nc-sa/3.0/"
__version__ = "1.0"
__maintainer__ = "Christopher Potts"
__email__ = "See the author's website"

######################################################################

import numpy, re
from collections import defaultdict
from factbank import *
import swda_experiment_clausetyping

######################################################################

def semprag_confusion_matrix(output_filename):
    """
    Build a confusion matrix comparing the FactBank annotations
    with the PragBank extension, limiting attention to cases
    where 6/10 agreed on a single category (which we then take
    to be the correct label). 

    The output CSV file has FactBank annotations as rows and the
    pragmatic annotations as columns.

    The output is the same as table III of de Marneffe et al.'s
    'Veridicality and utterance understanding'.
    """    
    # 2-d defaultdict for the counts:
    cm = defaultdict(lambda : defaultdict(int))
    # Instantiate the corpus:
    corpus = FactbankCorpusReader('fb-semprag.csv')
    # Iterate through the training set:
    for event in corpus.train_events():
        # Where defined, this will be a pair like (ct_plus, 7):
        pv, pv_count = event.majority_pragvalue()            
        # The AUTHOR-level factuality value is the most comparable to the pragmatic annotations:
        fv = event.FactValues['AUTHOR']
        # We limit attention to the items where the majority got at least 6 votes:
        if pv and pv_count >= 6:
            cm[fv][pv] += 1
    # CSV output with the FactBank annotations as rows and the
    # pragmatic annotations as columns:
    csvwriter = csv.writer(file(output_filename, 'w'))
    # Listing the keys like this ensures an intuitive ordering:
    keys = ['ct_plus', 'pr_plus', 'ps_plus', 'ct_minus', 'pr_minus', 'ps_minus', 'uu']
    csvwriter.writerow(['FactBank'] + keys)
    for fb in keys:
        row = [fb] + [cm[fb][pv] for pv in keys]
        csvwriter.writerow(row)
                     
# semprag_confusion_matrix('factbank-semprag-confusion-matrix.csv')

######################################################################

def nonauthor_factbank_annnotations():
    """Look at the strings associated with non-AUTHOR annotations in FactBank."""
    d = defaultdict(int)
    corpus = FactbankCorpusReader('fb-semprag.csv')
    for event in corpus.train_events():
        for src, fv in event.FactValues.items():
            if src != 'AUTHOR':
                d[src] += 1
    for key, val in sorted(d.items(), key=itemgetter(1), reverse=True):
        print key, val

# nonauthor_factbank_annnotations()

def author_nonauthor_factvalue_compare():
    """Compare FactBank AUTHOR and non-AUTHOR annotations for the same event."""
    d = defaultdict(int)
    corpus = FactbankCorpusReader('fb-semprag.csv')
    for event in corpus.train_events():
        fvs = event.FactValues
        auth =  fvs['AUTHOR']
        for src, fv in fvs.items():
            if src != 'AUTHOR':
                d[(auth, fv)] += 1
    keys = ['ct_plus', 'pr_plus', 'ps_plus', 'ct_minus', 'pr_minus', 'ps_minus', 'uu']
    # Little function for displaying neat columns:
    def fmt(a):
        return "".join(map((lambda x : str(x).rjust(14)), a))
    # Output printing:
    print fmt(['author\other'] + keys)
    for auth in keys:
        row = [auth]
        for other in keys:
            row.append(d[(auth, other)])
        print fmt(row)
    
# author_nonauthor_factvalue_compare()

######################################################################

def lexical_associations(n=10):
    """
    This function looks for words that are unusually over-represented
    in the FactBank (PragBank) annotations.

    The output is the top n items for each tag (default n=10).
    
    To do this, it iterates through the subset of the training set
    where there was a 6/10 majority choice label selected by the
    Turkers.

    For each event, it iterates through the words in the sentence for
    that event, adding 1 for (factbank-label, word) pairs and
    subtracting 1 for (pragbank-label, word) pairs.

    Thus, if the two sets of annotations were the same, these values
    would all be 0.  What we see instead is a lot of lexical variation
    (though the results are somewhat marred by the tendency for
    high-frequency words to end up with very large counts.
    """
    # Keep track of the differences:
    diff = defaultdict(lambda : defaultdict(int))
    # Instantiate the corpus:
    corpus = FactbankCorpusReader('fb-semprag.csv')    
    # Limit to the training set:
    events = corpus.train_events()
    # Limit to the events with at least a 6/10 majority choice:
    events = filter((lambda e : e.majority_pragvalue()[1] and e.majority_pragvalue()[1] >= 6), events)
    # Iterate through this restricted set of events:    
    for event in events:
        # Lemmatize:
        event_words = event.leaves(wn_lemmatize=True)
        # Remove punctuation, so that we look only at real words:
        event_words = filter((lambda x : not re.search(r"\W", x)), event_words)
        # Downcase:
        event_words = map(str.lower, event_words)
        #  Word counting:
        for word in event_words:
            diff[event.FactValues['AUTHOR']][word] += 1
            diff[event.majority_pragvalue()[0]][word] += 1
    # Function for formatting the results:
    def fmt(a):
        return ', '.join(map((lambda x : '%s: %s' % x), a))
    # View the results:
    keys = ['ct_plus', 'pr_plus', 'ps_plus', 'ct_minus', 'pr_minus', 'ps_minus', 'uu']
    for key in keys:
        sorted_vals = sorted(diff[key].items(), key=itemgetter(1))
        print key
        print '\tFactBank:', fmt(sorted(sorted_vals[-n:],  key=itemgetter(1), reverse=True)) # Put these in decreasing order.
        print '\tPragBank:', fmt(sorted_vals[:n])
    
# lexical_associations(n=10)

######################################################################

def tree_has_modal_daughter(tree):
    """
    If tree has a preterminal daughter whose terminal is a modal,
    return that modal, else return False.
    """
    modal_re = re.compile(r'^(Can|Could|Shall|Should|Will|Would|May|Might|Must|Wo)$', re.I)
    for daught in tree:
        if swda_experiment_clausetyping.is_preterminal(daught) and modal_re.search(daught[0]):
            return daught[0]
    return False

def c_commanding_modals(tree, terminal):
    """Return the set of modals that c-command terminal in tree."""
    modals = set([])
    for subtree in tree.subtrees():
        md = tree_has_modal_daughter(subtree)
        if md:
            if terminal in subtree.leaves():
                modals.add(md)
    return modals

def modal_stats(factbank_or_pragbank):
    """
    Gather and print a matrix relating modal use (rows) to
    veridicality values:

    factbank_or_pragbank (str) -- if 'factbank' (case-insensitive),
                                  then use the FactBank annotations,
                                  else use the PragBank majority annotation

    The calculations are limited to the subset of the events that have
    a 6/10 majority category in PragBank, to facilitate comparisons
    between the two annotation groups.
    """
    
    corpus = FactbankCorpusReader('fb-semprag.csv')    
    # Limit to the training set:
    events = corpus.train_events()
    # Limit to the events with at least a 6/10 majority choice:
    events = filter((lambda e : e.majority_pragvalue()[1] and e.majority_pragvalue()[1] >= 6), events)
    # For the counts:
    counts = defaultdict(lambda : defaultdict(int))
    # Iterate through the events:
    for event in events:
        modals = c_commanding_modals(event.SentenceParse, event.eText)
        for modal in modals:
            val = None
            if factbank_or_pragbank.lower() == 'factbank':
                val = event.FactValues['AUTHOR']
            else:
                val = event.majority_pragvalue()[0]
            counts[modal][val] += 1
    # Modals:
    modals = sorted(counts.keys())
    # Categories:
    keys = ['ct_plus', 'pr_plus', 'ps_plus', 'ct_minus', 'pr_minus', 'ps_minus', 'uu']
    # Little function for displaying neat columns:
    def fmt(a):
        return "".join(map((lambda x : str(x).rjust(10)), a))
    # Output printing:
    print "======================================================================"
    print factbank_or_pragbank
    print fmt([''] + keys)
    for modal in modals:
        row = [modal]
        for cat in keys:
            row.append(counts[modal][cat])
        print fmt(row)
    
modal_stats('FactBank')
modal_stats('PragBank')

