from hazm import word_tokenize, Lemmatizer
import string

#TODO: load another corpus
def load_corpus(data_path):
    with open(data_path, "r", encoding="utf-8") as corpus:
            corpus = corpus.read()
    return corpus


#TODO: lemma, space_to_space
def tokenize(corpus,lemma=True, punctuation=True, space_to_space=True):

    if(not punctuation):
        table = str.maketrans({key: None for key in string.punctuation})
        corpus = corpus.translate(table)   

    tokenized = word_tokenize(corpus)
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

def generate_sentence():
    return

def perplexity():
    return

corpus = load_corpus("corpus.txt")
tokenized = tokenize(corpus,punctuation=False)
ngrams = generate_n_gram(tokenized, 4)
ngrams_minus_1 = generate_n_gram(tokenized, 3)
