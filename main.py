from hazm import word_tokenize, Lemmatizer
from numpy.random import choice
import string
import math


def load_corpus(data_path):
    with open(data_path, "r", encoding="utf-8") as corpus:
            corpus = corpus.read()
    return corpus

def tokenize(corpus,lemma=True, punctuation=True, space_to_space=False):

    if(not punctuation):
        # table = str.maketrans({key: None for key in string.punctuation})
        # corpus = corpus.translate(table)
        corpus = corpus.replace(',', ' ')
        corpus=corpus.replace("\u220c","")
        corpus = corpus.replace('(', ' ')
        corpus = corpus.replace(')', ' ')
        corpus = corpus.replace('.', ' ')
        corpus=corpus.replace("،"," ")
        corpus=corpus.replace("«"," ")
        corpus=corpus.replace("»"," ")

    if(space_to_space):
        tokenized = corpus.split(' ')
    else:    
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
    sum_log_probs = 0
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
        sum_log_probs = sum_log_probs + math.log(probs[options.index(winner)],2)
        i=i+1

    #perplexity= math.pow((1/multiplied_probs),(1/len(sentence)))
    perplexity_by_log= 2** (-1.0 * sum_log_probs / len(sentence))

    # print(perplexity, perplexity_by_log)
    return sentence, perplexity_by_log

def generate_all_sentences(tokenized):
    sentences = []
    result = ''

    for n in range(2,6):
        ngrams = generate_n_gram(tokenized, n)
        ngrams_minus_1 = generate_n_gram(tokenized, n-1)
        for j in range(10):
            if(n==2):
                sentence, perplexity_by_log = generate_sentence(n=n,start_words=['<S>'] ,ngrams=ngrams, ngrams_minus_1=ngrams_minus_1)
                sentences.append(sentence)

            if(not n==2):
                sentence, perplexity_by_log = generate_sentence(n=n,start_words=sentences[(n-3)*10+j][0:n-1] ,ngrams=ngrams, ngrams_minus_1=ngrams_minus_1)
                sentences.append(sentence)

            # print('ngram: ', n, 'sentence: ', sentence, 'perplexity: ', perplexity, 'perplexity_by_log: ',perplexity_by_log)

            result = result+ '\nn: '+ str(n)
            result = result+'\t'+' '.join(sentence)
            result = result+ '\nperplexity: ' + str(perplexity_by_log)

    return result

def compute_test_perplexity(n, test_tokenized, tokenized):
    
    ngrams = generate_n_gram(tokenized, n)
    ngrams_minus_1 = generate_n_gram(tokenized, n-1)

    sum_log_probs = 0
    for i in range(len(test_tokenized)):

        found = False
        for ngram in ngrams:
            if ngram[0] == test_tokenized[i-n:i]:
                count_ngram = ngram[1]
                found = True
        
        if(not found):
            prob = 1
        else:
            for ngram_1 in ngrams_minus_1:
                if ngram_1[0] == test_tokenized[i-n:i-1]:
                    prob = count_ngram / ngram_1[1]

        sum_log_probs = sum_log_probs + math.log(prob,2)

    perplexity_by_log= 2** (-1.0 * sum_log_probs / len(test_tokenized))

    print (perplexity_by_log)

    return 

def generate_unigram_sentences(tokenized):
    unigrams = []
    result = ''
    vocab = set(tokenized)
    
    for word in vocab:
        unigrams.append((word,tokenized.count(word)/len(vocab)))


    for j in range(100):
        sentence = []
        i=0
        sum_log_probs = 0
        while ( (len(sentence)==0 or not sentence[-1]=='</S>') and len(sentence)<15) :

            options=[i[0] for i in unigrams]
            probs=[i[1] for i in unigrams]

            winner = choice(options, 1, probs)
            sentence.append(winner[0])

            sum_log_probs = sum_log_probs + math.log(probs[options.index(winner)],2)
            i=i+1

            
        perplexity_by_log= 2** (-1.0 * sum_log_probs / len(sentence))

        result = result+ '\nn:  1'
        result = result+'\t'+' '.join(sentence)
        result = result+ '\nperplexity: ' + str(perplexity_by_log)

    return  result

def compute_unigram_test_perplexity(test_tokenized, tokenized):

    unigrams = []
    vocab = set(tokenized)
    
    for word in vocab:
        unigrams.append((word,tokenized.count(word)/len(vocab)))


    sum_log_probs = 0
    for i in range(len(test_tokenized)):
        
        for unigram in unigrams:
            if(unigram[0]==test_tokenized[i]):
                prob = unigram[1]

        sum_log_probs = sum_log_probs + math.log(prob,2)

    perplexity_by_log= 2** (-1.0 * sum_log_probs / len(test_tokenized))

    print (perplexity_by_log)
    return

# load and token
corpus = load_corpus("train.txt")
tokenized = tokenize(corpus,lemma=False, punctuation=False)

# generate sentences n-gram
# result = generate_all_sentences(tokenized)
# result = generate_unigram_sentences(tokenized)
# f= open("ngram_sentenses.txt","w+")
# f.write(result)
# f.close()


## Test
corpus = load_corpus("train3.txt")
tokenized = tokenize(corpus,lemma=True, punctuation=True)

corpus = load_corpus("test.txt")
test_tokenized = tokenize(corpus,lemma=True, punctuation=True)
# compute_test_perplexity(n=4, test_tokenized=test_tokenized, tokenized=tokenized)
compute_unigram_test_perplexity(test_tokenized, tokenized)