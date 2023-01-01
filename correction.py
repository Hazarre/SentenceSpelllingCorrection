import re
import math
from collections import Counter

def words(text): return re.findall(r'\w+', text.lower())

WORDS = Counter(words(open('big.txt').read()))

def P(word, n=sum(WORDS.values())): 
    "Probability of `word`."
    return WORDS[word] / n

def correction(word): 
    "Most probable spelling correction for word."
    return max(candidates(word), key=P)

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return list(set(w for w in words if w in WORDS))

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return deletes + transposes + replaces + inserts

def edits2(word): 
    "All edits that are two edits away from `word`."
    return [e2 for e1 in edits1(word) for e2 in edits1(e1)]

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def gen_candidates(word): 
    "Generate possible spelling corrections for word."
    return list( set( known(edits1(word)) + known(edits2(word)) + known([word]) )) 

def gen_ngram(n, trainfile):
    # return a dictionary to look up ngram model with log probability 
    infile = open(trainfile, "r+")
    count = 0 
    ngrams = {}
    for line in infile:
        line = ['<s>']*n + [w.lower() for w in line.split()] + ['<\s>']*n 
        for i in range( len(line) - n ):
            k = tuple(line[i:i+n])
            v = line[i+n]
            if k in ngrams.keys():
                if v in ngrams[k]:
                    ngrams[k][v] += 1
                else:
                    ngrams[k][v] =1
            else:
                ngrams[k] = {v: 1}
    for k in ngrams.keys():
        count = 0 
        for prec in ngrams[k].keys():
            count += ngrams[k][prec]        
        ngrams[k]["<total>"] = count
    return ngrams


def Pngram(n, sentence, ngrams): 
    # log probability of the ngram model of a sentence. 
    p = 0 
    l = len(sentence)
    for i in range(l - n): 
        k = tuple(sentence[i:i+n])
        v = sentence[i+n]
        if k in ngrams.keys():
            if v in ngrams[k]: 
                p += math.log( ngrams[k][v]/ngrams[k]["<total>"])
            else:
                p += math.log( (1 / ngrams[k]["<total>"]))
        else:
            p += -10
    return p



N = 2
NGRAM = gen_ngram(N, "big.txt")
def correct_sentence(sentence, n=N, alpha=.95):
    l = len(sentence)
    if l < 1:
        return []
    l += n*2
    sentence = n*["<s>"] + sentence + n*["<\s>"]

    # find candidate probability
    best_candidate = sentence[0]
    error_at = 0
    max_likelihood = -9999999

    # find most likely candidate sentence
    for i in range(l): 
        ob = sentence[i]
        correction_candidates = gen_candidates(ob)
        ncandidates = len(correction_candidates)
        for c in correction_candidates:
            likelihood = 0
            sentence[i] = c
            prior = Pngram(n, sentence, NGRAM)
            error = alpha if ob == c else (1-alpha) / ncandidates
            likelihood = math.log(error) + prior 
            # print(c , likelihood, sentence)
            sentence[i] = ob

            if likelihood > max_likelihood: 
                print("found max", c)
                max_likelihood = likelihood
                best_candidate = c
                error_at = i

    # apply correction 
    sentence[error_at] = best_candidate
    return sentence

# optW = argmax P(X|W) P(W), for W in C(X)
# P(W): use bigram or trigram probability
# alpha 

# P(X|W) 
# = alpha,  x=w
# = 1 - alpha / |C(x)|
# = 0 other wise 


if __name__ == '__main__':
    count = 0
    alpha_values = [.99, .95, .90, .80, .70, .60, .50, .40, .30, .20]

    # for a in alpha_values:
        # f = open("realword_error.txt", "r+")
        # outfile = open("realworld_corrected%.2f.txt" % a, "w+")
        # for line in f:
        #     sent = line.split()
        #     corrected = correct_sentence(sent, N , a)
        #     l = len(corrected)
        #     if l > N:
        #         outfile.write(" ".join(corrected[N:-N]))
        #         outfile.write("\n") 
        # outfile.close()
        # f.close()

    # print( Pngram(N, N*["<s>"] + ["I"], NGRAM) )
    # print( Pngram(N, N*["<s>"] + ["i"], NGRAM) )
    # sent1 = ["i", "am", "there", "years", "old"]
    # sent2 = ["i", "have", "an", "apply"]
    # sent3 = ["i", "have", "an", "apple"]

    sent  = ["only", "two", "of", "thew", "apples"]
    corrected = correct_sentence(sent, N)
    print(corrected)

    # print( Pngram(N, N*["<s>"] + sent2 +N*["<s>"] , NGRAM) )
    # print( Pngram(N, N*["<s>"] + sent3 +N*["<s>"] , NGRAM) )
    