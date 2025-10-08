import streamlit as st
from preprocessing.tokenizer_stemmer import preprocess_user_input, reconstruct_sentence
from rules.correction_dict import correction_dict
# from preprocessing.grammar_detector import detect_errors
from rules.regex_rules import apply_regex_rules, regex_patterns
import re

# -------------------------
# Streamlit UI
# -------------------------
st.title("Bengali Grammar Corrector (All Layers Highlighted)")

user_input = st.text_input("Enter a Bengali sentence:")

# -------------------------
# Highlight dictionary / POS corrections in red
# -------------------------
def highlight_tokens(tokens, corrections_dict, color="red"):
    highlighted = []
    for tok in tokens:
        corrected_tok = corrections_dict.get(tok, tok)
        if corrected_tok != tok:
            highlighted.append(f'<span style="color:{color};font-weight:bold">{corrected_tok}</span>')
        else:
            highlighted.append(tok)
    return highlighted

# -------------------------
# Highlight regex corrections in blue
# -------------------------
def highlight_regex_corrections(text, regex_rules):
    """
    Apply regex rules to text and highlight changes in blue.
    """
    for pattern, replacement in regex_rules:
        text = re.sub(pattern, lambda m: f'<span style="color:blue;font-weight:bold">{replacement}</span>', text)
    return text

# -------------------------
# Button action
# -------------------------
if st.button("Correct"):
    if user_input.strip() == "":
        st.warning("Please enter a sentence.")
    else:
        # Step 1: Preprocess input
        tokens = preprocess_user_input(user_input)

        # Step 2: POS-based dynamic corrections
        # suggestions = detect_errors(user_input)
        # pos_corrections = {}
        # for wrong, correct in suggestions:
        #     if wrong != "missing_ki":
        #         pos_corrections[wrong] = correct
        #     else:
        #         # Insert 'কি' after first word for yes/no questions
        #         parts = tokens.copy()
        #         parts.insert(1, correct)
        #         tokens = parts

        # # Step 3: Merge dictionary + POS corrections
        # combined_corrections = {**correction_dict, **pos_corrections}

        # Step 4: Apply and highlight dictionary + POS corrections
        # corrected_tokens = highlight_tokens(tokens, combined_corrections, color="red")
        corrected_tokens = highlight_tokens(tokens, correction_dict, color="red")
        corrected_sentence = reconstruct_sentence(corrected_tokens)

        # Step 5: Apply regex-based corrections and highlight in blue
        corrected_sentence = highlight_regex_corrections(corrected_sentence, regex_patterns)

        # -------------------------
        # Display results
        # -------------------------
        st.subheader("Original Sentence:")
        st.write(user_input)

        st.subheader("Corrected Sentence (Red = Dict/POS, Blue = Regex):")
        st.markdown(corrected_sentence, unsafe_allow_html=True)
