# rules/auto_expand_dict.py
import pandas as pd
from difflib import SequenceMatcher
import ast

def auto_expand_corrections(dataset_path, correction_dict_path):
    """
    Expands correction_dict.py using dataset pairs (incorrect, correct).
    Writes new rules back into correction_dict.py if new pairs are found.
    """
    # --- Step 1: Load existing dictionary ---
    with open(correction_dict_path, "r", encoding="utf-8") as f:
        content = f.read()

    start = content.find("{")
    end = content.rfind("}") + 1
    correction_dict = ast.literal_eval(content[start:end])

    # --- Step 2: Load dataset correctly ---
    df = pd.read_csv(dataset_path, sep='\t')  # ✅ FIXED — using variable not undefined name
    new_pairs = 0

    # --- Step 3: Learn new corrections ---
    for _, row in df.iterrows():
        if "incorrect" in row and "correct" in row:
            incorrect, correct = row["incorrect"], row["correct"]
            ratio = SequenceMatcher(None, incorrect, correct).ratio()

            if ratio < 1.0 and incorrect not in correction_dict:
                correction_dict[incorrect] = correct
                new_pairs += 1

    # --- Step 4: Rewrite dictionary if new pairs found ---
    if new_pairs > 0:
        with open(correction_dict_path, "w", encoding="utf-8") as f:
            f.write("# Auto-updated correction dictionary\n")
            f.write("correction_dict = {\n")
            for k, v in correction_dict.items():
                f.write(f"    {repr(k)}: {repr(v)},\n")
            f.write("}\n")
        print(f"✅ Added {new_pairs} new corrections to correction_dict.py")
    else:
        print("No new corrections found — dictionary already up to date.")

    return correction_dict
