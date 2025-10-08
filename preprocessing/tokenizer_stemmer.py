import pandas as pd
from bnltk.tokenize import Tokenizers
from preprocessing.stopwords import stopwords_bn
from rules.correction_dict import correction_dict
import string

t = Tokenizers()

# -------------------------
# Preprocessing function for user input (Rule-Based)
# -------------------------
def preprocess_user_input(text):
    """
    Tokenize and remove stopwords/punctuation,
    but DO NOT stem for rule-based correction.
    """
    tokens = t.bn_word_tokenizer(text)
    filtered = [tok for tok in tokens if tok not in stopwords_bn and tok not in string.punctuation]
    return filtered  # keep original tokens intact

# -------------------------
# Correction function
# -------------------------
def correct_sentence(tokens):
    """
    Return a list where corrected words are wrapped in '**' to highlight in Markdown.
    """
    corrected_tokens = []
    for tok in tokens:
        corrected_tok = correction_dict.get(tok, tok)
        if corrected_tok != tok:
            # wrap changed word in bold
            corrected_tokens.append(f'<span style="color:red;font-weight:bold">{corrected_tok}</span>')
        else:
            corrected_tokens.append(tok)
    return corrected_tokens

# -------------------------
# Reconstruct sentence
# -------------------------
def reconstruct_sentence(tokens):
    return " ".join(tokens)

# -------------------------
# Functions for dataset preprocessing (optional)
# -------------------------
from bnltk.stemmer import BanglaStemmer
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
