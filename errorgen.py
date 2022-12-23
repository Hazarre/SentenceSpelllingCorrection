import re
from collections import Counter
import random 


# this file generates one spelling error per sentence for a input text file. 

# the spelling errors are generated with edit distance 1 and 2. 


def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return list(set(deletes + transposes + replaces + inserts))

def edits2(word): 
    "All edits that are two edits away from `word`."
    return [e2 for e1 in edits1(word) for e2 in edits1(e1)]

def parsePair(lines):
    errors = {}
    "Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs."
    for line in lines:
        print(line)
        break
        right, wrongs = line.strip().split(':')
        errors[right] = wrongs.split()
    return errors


def corruptWord(word):
    p = .9
    if random.random() <= p:
        edits = edits1(word)
    else: 
        edits = edits2(word)
    l = len(edits)
    return random.choice(edits)


def genError(fname): 
    count = 0 
    lines = open(fname + ".txt")
    outfile = open(fname + "Error.txt" , "r+")

    for line in lines: 
        words = line.split()
        l = len(words) 
        print(count, words)
        if (l > 1): 
            e = random.randrange(l)
            error = corruptWord(words[e])
            words[e] = error
            outfile.write(" ".join(words))        
            outfile.write("\n")        
        else: 
            outfile.write("\n")
      
        # count += 1
        # if count == 3: 
        #     break

if __name__ == '__main__':
    genError("greatGatsbyChp1")


    