# rules/auto_pos_rule_generator.py
import pandas as pd
from difflib import SequenceMatcher
from collections import Counter
import ast
import stanza
from pathlib import Path

# -------------------------
# Local Stanza resources
# -------------------------
STANZA_MODEL_DIR = r"C:\Users\ADMIN\stanza_resources"  # <-- update this path

if not Path(STANZA_MODEL_DIR).exists():
    raise FileNotFoundError(f"Stanza resources folder not found at {STANZA_MODEL_DIR}")

# Initialize Bengali NLP pipeline offline
nlp = stanza.Pipeline(
    lang='bn',
    processors='tokenize,pos',
    tokenize_no_ssplit=True,
    dir=STANZA_MODEL_DIR,
    use_gpu=False,
    verbose=False
)

# -------------------------
# POS tagging function
# -------------------------
def pos_tag(text):
    """Return a list of (word, POS) tuples using Stanza."""
    doc = nlp(text)
    return [(word.text, word.pos) for sent in doc.sentences for word in sent.words]

# -------------------------
# Main auto POS-rule generator
# -------------------------
def generate_pos_rules(dataset_path, correction_dict_path, freq_threshold=3):
    """
    Extract frequent POS-based grammar mistakes from dataset
    and automatically update correction_dict.py
    """
    # --- Step 1: Load dataset ---
    df = pd.read_csv(dataset_path)
    if 'incorrect' not in df.columns or 'correct' not in df.columns:
        raise ValueError("Dataset must have 'incorrect' and 'correct' columns")
    
    # --- Step 2: Load existing correction dict ---
    with open(correction_dict_path, "r", encoding="utf-8") as f:
        content = f.read()
    start = content.find("{")
    end = content.rfind("}") + 1
    correction_dict = ast.literal_eval(content[start:end])

    # --- Step 3: Extract mistakes with POS ---
    pattern_counter = Counter()
    changes = []

    for _, row in df.iterrows():
        inc_words = row['incorrect'].split()
        cor_words = row['correct'].split()
        matcher = SequenceMatcher(None, inc_words, cor_words)

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag != 'equal':
                wrong_chunk = ' '.join(inc_words[i1:i2])
                correct_chunk = ' '.join(cor_words[j1:j2])
                pos_tags = tuple(t for _, t in pos_tag(wrong_chunk))
                changes.append((pos_tags, wrong_chunk, correct_chunk))
                pattern_counter[(pos_tags, wrong_chunk)] += 1

    # --- Step 4: Generate auto rules from frequent patterns ---
    new_pairs = 0
    auto_rules = {}

    for (pos_seq, wrong), freq in pattern_counter.items():
        if freq >= freq_threshold and wrong not in correction_dict:
            corrected = None
            # Verb rules
            if pos_seq and pos_seq[-1].startswith("VERB"):
                if wrong.endswith("তেছি"):
                    corrected = wrong[:-4] + "ছি"
                elif wrong.endswith("তেছে"):
                    corrected = wrong[:-4] + "ছে"
            # Yes/No question missing 'কি'
            if wrong.endswith("?") and not wrong.startswith("কি"):
                auto_rules["missing_ki"] = "কি"
            
            if corrected:
                auto_rules[wrong] = corrected
                new_pairs += 1

    # --- Step 5: Update correction dictionary ---
    correction_dict.update(auto_rules)
    if new_pairs > 0:
        with open(correction_dict_path, "w", encoding="utf-8") as f:
            f.write("# Auto-updated correction dictionary (POS-rule based)\n")
            f.write("correction_dict = {\n")
            for k, v in correction_dict.items():
                f.write(f"    {repr(k)}: {repr(v)},\n")
            f.write("}\n")
        print(f"✅ Added {new_pairs} new POS-based corrections to correction_dict.py")
    else:
        print("No new frequent POS-based corrections found.")

    return correction_dict
