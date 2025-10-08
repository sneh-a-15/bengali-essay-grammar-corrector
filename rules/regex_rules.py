# rules/regex_rules.py
import re

# -------------------------
# List of patterns + replacements for highlighting
# -------------------------
regex_patterns = [
    (r'(\w+)তেছে', r'\1ছে'),
    (r'(\w+)তেছিলাম', r'\1ছিলাম'),
    (r'(\w+)ছিলা', r'\1ছিল'),
    (r'হইতেছে', 'হচ্ছে'),
    (r'খাইতেছি', 'খাচ্ছি')
]

# -------------------------
# Function to apply regex corrections
# -------------------------
def apply_regex_rules(text):
    for pattern, replacement in regex_patterns:
        text = re.sub(pattern, replacement, text)
    return text
