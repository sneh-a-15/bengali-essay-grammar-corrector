import pandas as pd
from bnltk.tokenize import Tokenizers
from bnltk.stemmer import BanglaStemmer
import string
from preprocessing.stopwords import stopwords_bn

t = Tokenizers()
bn_stemmer = BanglaStemmer()

def tokenize_and_stem(text):
    """Tokenize and stem a Bengali sentence."""
    if pd.isna(text):
        return []
    tokens = t.bn_word_tokenizer(text)
    stemmed = [bn_stemmer.stem(tok) for tok in tokens]
    return stemmed

def clean_tokens(text):
    """Tokenize, remove stopwords/punctuation, and stem."""
    if pd.isna(text):
        return []
    tokens = t.bn_word_tokenizer(text)
    filtered = [tok for tok in tokens if tok not in stopwords_bn and tok not in string.punctuation]
    stemmed = [bn_stemmer.stem(tok) for tok in filtered]
    return stemmed
