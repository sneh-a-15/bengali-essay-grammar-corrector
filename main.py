# from preprocessing.grammar_detector import detect_errors
from rules.regex_rules import apply_regex_rules
from rules.auto_expand_dict import auto_expand_corrections
# from rules.auto_pos_rule_generator import generate_pos_rules
from rules.correction_dict import correction_dict

DATA_PATH = "data/bengali_grammar_autocorrect_dataset.csv"
DICT_PATH = "rules/correction_dict.py"

def correct_text(text):
    # Step 0: Detect grammar errors dynamically
    # suggestions = detect_errors(text)
    # for wrong, correct in suggestions:
    #     if wrong != "missing_ki":
    #         text = text.replace(wrong, correct)
    #     else:
    #         parts = text.split(" ")
    #         parts.insert(1, correct)
    #         text = " ".join(parts)

    # Step 1: Apply dictionary replacements
    for wrong, right in correction_dict.items():
        text = text.replace(wrong, right)
    
    # Step 2: Apply regex-based transformations
    text = apply_regex_rules(text)
    return text

if __name__ == "__main__":
    # --- Auto-update correction dictionary ---
    auto_expand_corrections(DATA_PATH, DICT_PATH)
    # generate_pos_rules(DATA_PATH, DICT_PATH, freq_threshold=3)

    # --- Test sample ---
    sample_text = "আমি যাইতে পারবো না, সে খাইতেছে।"
    corrected_text = correct_text(sample_text)

    print("Before:", sample_text)
    print("After :", corrected_text)
