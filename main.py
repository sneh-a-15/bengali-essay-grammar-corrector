import sys
sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
from preprocessing.tokenizer_stemmer import tokenize_and_stem, clean_tokens

print("বাংলা ভাষা খুবই সুন্দর।")
# Load dataset
df = pd.read_csv('data/bengali_grammar_autocorrect_dataset.csv')

# Apply preprocessing
df['incorrect_cleaned'] = df['incorrect'].apply(clean_tokens)
df['correct_cleaned'] = df['correct'].apply(clean_tokens)

# Save processed data
df.to_csv('data/cleaned_data.csv', index=False)

print(df.head())
