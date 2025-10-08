# preprocessing/grammar_detector.py
import stanza
from pathlib import Path

# -------------------------
# Path to your local Stanza resources
# -------------------------
STANZA_MODEL_DIR = r"C:\Users\ADMIN\stanza_resources"

if not Path(STANZA_MODEL_DIR).exists():
    raise FileNotFoundError(f"Stanza model folder not found at {STANZA_MODEL_DIR}")

# Initialize Bengali pipeline OFFLINE
bn_pipeline = stanza.Pipeline(
    lang='bn',
    processors='tokenize,pos',
    dir=STANZA_MODEL_DIR,
    use_gpu=False,
    verbose=False,
    download_method=None
)

def detect_errors(text):
    """
    Detects Bengali grammar mistakes dynamically using POS patterns.
    Returns a list of (wrong, correct) tuples.
    """
    suggestions = []
    doc = bn_pipeline(text)

    tokens = []
    if doc.sentences:
        tokens = [(word.text, word.upos) for sent in doc.sentences for word in sent.words]

    for i, (word, tag) in enumerate(tokens):
        # Rule 1: Continuous tense (তেছি → ছি)
        if tag.startswith("VERB") and word.endswith("তেছি"):
            suggestions.append((word, word[:-4] + "ছি"))

        # Rule 2: Continuous tense (তেছে →ছে)
        elif tag.startswith("VERB") and word.endswith("তেছে"):
            suggestions.append((word, word[:-4] + "ছে"))

        # Rule 3: Yes/No question missing 'কি'
        if text.endswith("?") and "কি" not in [w for w, t in tokens[:3]]:
            suggestions.append(("missing_ki", "কি"))

    return suggestions
