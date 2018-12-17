from hazm import word_tokenize, Lemmatizer
import string


def load_corpus(data_path):
    with open(data_path, "r", encoding="utf-8") as corpus:
            corpus = corpus.read()
    return corpus

def tokenize(corpus,lemma=True, punctuation=True, space_to_space=True):

    if(not punctuation):
        table = str.maketrans({key: None for key in string.punctuation})
        corpus = corpus.translate(table)   

    tokenized = word_tokenize(corpus)
    return tokenized

def generate_n_gram(tokenized):
    return

def generate_sentence():
    return

def perplexity():
    return

corpus = load_corpus("corpus.txt")
tokenized = tokenize(corpus,punctuation=False)
print(tokenized)
