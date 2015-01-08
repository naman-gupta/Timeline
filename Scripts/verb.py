from nltk.stem.wordnet import WordNetLemmatizer
import sys
from nltk.corpus import verbnet

def abc():
    verbWord=sys.argv[1]
    lmtzr = WordNetLemmatizer()
    verbLemma = lmtzr.lemmatize(verbWord,'v')
    classIds = verbnet.classids(verbLemma)
    print classIds
    if(len(classIds)>0):
        ids = classIds[0]
        verbclassId = ids.split("-")[0]
        print verbWord," ",verbclassId
    else:
        print verbWord," ","_null_"

if __name__ == '__main__':
    ip = ''
    #inputfile = open('list.txt', 'r')
    #lmtzr = WordNetLemmatizer()
    #for line in inputfile:
    #    abc(line.strip())
    abc()
