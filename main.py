from hazm import word_tokenize, Lemmatizer
from numpy.random import choice
import string
import math

#TODO: load another corpus
def load_corpus(data_path):
    with open(data_path, "r", encoding="utf-8") as corpus:
            corpus = corpus.read()
    return corpus

#TODO: space_to_space
def tokenize(corpus,lemma=True, punctuation=True, space_to_space=True):

    if(not punctuation):
        table = str.maketrans({key: None for key in string.punctuation})
        corpus = corpus.translate(table)

    tokenized = word_tokenize(corpus)

    if(lemma):
        lemmatizer=Lemmatizer()
        for i in range(len(tokenized)):
            tokenized[i] = lemmatizer.lemmatize(tokenized[i]).split('#')[0]

    print(tokenized)
    return tokenized

def generate_n_gram(tokenized, n):
    ngrams_list = []
    ngrams = []
 
    for num in range(len(tokenized)):
        ngram=(tokenized[num:num + n])
        ngrams_list.append(ngram)

    for i in range(len(ngrams_list)):
        flag = False
        for j in range(len(ngrams)):
            if  ngrams[j][0]==ngrams_list[i]:
                flag = True
        if not flag:
            ngrams.append((ngrams_list[i],ngrams_list.count(ngrams_list[i])))

    return ngrams

#TODO: end of sentense condition
#TODO: 3gram and more
def generate_sentence(n, start_word, ngrams, ngrams_minus_1):
    sentence = [start_word]
    m= 5
    multiplied_probs =1

    for i in range(m):
        options = []
        probs = []

        for ngram_1 in ngrams_minus_1:
            if ngram_1[0]== sentence[i:i+n-1]:
                count_ngram_minus_1 = ngram_1[1]

        for ngram in ngrams:
            if ngram[0][0:n-1]== sentence[i:i+n-1]:
                options.append(ngram[0][n-1])
                probs.append(ngram[1]/count_ngram_minus_1)

        
        winner = choice(options, 1, probs)
        sentence.append(winner[0])
        multiplied_probs = multiplied_probs * probs[options.index(winner)]

    perplexity= math.pow((1/multiplied_probs),(1/m))

    return sentence,perplexity

# n-gram
n = 2

corpus = load_corpus("corpus.txt")
tokenized = tokenize(corpus,punctuation=False)
# ngrams = generate_n_gram(tokenized, n)
# ngrams_minus_1 = generate_n_gram(tokenized, n-1)
# sentence, perplexity = generate_sentence(n=n,start_word='و' ,ngrams=ngrams, ngrams_minus_1=ngrams_minus_1)
# print (sentence)
# print(perplexity)