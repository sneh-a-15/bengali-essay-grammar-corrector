from preprocessing.tokenizer_stemmer import clean_tokens
from rules.correction_dict import correction_dict

def correct_sentence(tokens):
    return [correction_dict.get(tok, tok) for tok in tokens]

def reconstruct_sentence(tokens):
    return " ".join(tokens)

user_input = input("Enter a Bengali sentence: ")
tokens = clean_tokens(user_input)
corrected_tokens = correct_sentence(tokens)
corrected_sentence = reconstruct_sentence(corrected_tokens)

print("Original:", user_input)
print("Corrected:", corrected_sentence)
