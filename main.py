from hazm import word_tokenize, Lemmatizer
from numpy.random import choice
import string
import math

def load_corpus(data_path):
    with open(data_path, "r", encoding="utf-8") as corpus:
            corpus = corpus.read()
    return corpus

#TODO: space_to_space
#TODO: don't remove < >
def tokenize(corpus,lemma=True, punctuation=True, space_to_space=True):

    if(not punctuation):
        table = str.maketrans({key: None for key in string.punctuation})
        corpus = corpus.translate(table)

    tokenized = word_tokenize(corpus)

    if(lemma):
        lemmatizer=Lemmatizer()
        for i in range(len(tokenized)):
            tokenized[i] = lemmatizer.lemmatize(tokenized[i]).split('#')[0]

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

def generate_sentence(n, start_words, ngrams, ngrams_minus_1):
    sentence = start_words
    multiplied_probs =1
    i=0

    while not sentence[-1]=='</S>':
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
        i=i+1

    perplexity= math.pow((1/multiplied_probs),(1/len(sentence)))

    return sentence,perplexity

# n-gram
n = 3

corpus = load_corpus("test.txt")
tokenized = tokenize(corpus,lemma=False, punctuation=True)


# ngrams = generate_n_gram(tokenized, n)
# ngrams_minus_1 = generate_n_gram(tokenized, n-1)
# sentence, perplexity = generate_sentence(n=n,start_words=['<S>','و'] ,ngrams=ngrams, ngrams_minus_1=ngrams_minus_1)
# print (sentence)
# print(perplexity)

sentences = []

for n in range(1,6):
    for j in range(10):
        print(n, j)
        ngrams = generate_n_gram(tokenized, n)
        ngrams_minus_1 = generate_n_gram(tokenized, n-1)

        if(n==1):
            sentence, perplexity = generate_sentence(n=n,start_words=[] ,ngrams=ngrams, ngrams_minus_1=ngrams_minus_1)

        if(n==2):
            sentence, perplexity = generate_sentence(n=n,start_words=['<S>'] ,ngrams=ngrams, ngrams_minus_1=ngrams_minus_1)
            sentences.append(sentence)

        if(not n==1 and not n==2):
            sentence, perplexity = generate_sentence(n=n,start_words=sentences[(n-3)*10+j][0:n-1] ,ngrams=ngrams, ngrams_minus_1=ngrams_minus_1)
            sentences.append(sentence)

        print('ngram: ', n, 'sentence: ', sentence, 'perplexity: ', perplexity)