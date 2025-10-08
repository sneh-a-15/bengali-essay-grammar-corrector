import streamlit as st
from preprocessing.tokenizer_stemmer import preprocess_user_input, reconstruct_sentence
from rules.correction_dict import correction_dict

# Streamlit UI
st.title("Bengali Grammar Corrector (Rule-Based)")

user_input = st.text_input("Enter a Bengali sentence:")

# -------------------------
# Highlight corrections
# -------------------------
def highlight_corrections(tokens):
    """
    Highlight corrected words in red using the correction_dict.
    """
    highlighted_tokens = []
    for tok in tokens:
        corrected_tok = correction_dict.get(tok, tok)
        if corrected_tok != tok:
            # Highlight the corrected word in red and bold
            highlighted_tokens.append(f'<span style="color:green;font-weight:bold">{corrected_tok}</span>')
        else:
            highlighted_tokens.append(corrected_tok)
    return highlighted_tokens

# -------------------------
# Button action
# -------------------------
if st.button("Correct"):
    if user_input.strip() == "":
        st.warning("Please enter a sentence.")
    else:
        # Preprocess user input
        tokens = preprocess_user_input(user_input)
        # Highlight corrected tokens
        corrected_tokens = highlight_corrections(tokens)
        # Reconstruct the sentence
        corrected_sentence = " ".join(corrected_tokens)
        
        st.subheader("Original Sentence:")
        st.write(user_input)
        
        st.subheader("Corrected Sentence:")
        st.markdown(corrected_sentence, unsafe_allow_html=True)
