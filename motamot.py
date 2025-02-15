import streamlit as st
import gdown
import os
from gensim.models import KeyedVectors

# File and Google Drive settings
MODEL_PATH = "word2vec.model"
GOOGLE_DRIVE_ID = "1A2B3C4D5E6F7G8H9"  # Replace with your actual file ID

# 🔹 Function to download the model if it's missing
def download_model():
    if not os.path.exists(MODEL_PATH):
        st.info("📥 Downloading Word2Vec model... (only happens once)")
        url = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        st.success("✅ Model downloaded successfully!")

# 🔹 Load the model efficiently
@st.cache_resource
def load_model():
    download_model()  # Ensure model exists before loading
    return KeyedVectors.load(MODEL_PATH)

# 🔹 Load model
model = load_model()

# 🔹 Streamlit UI
st.title("🔍 Word2Vec Similarity Checker")

word1 = st.text_input("Enter first word:")
word2 = st.text_input("Enter second word:")

if st.button("Check Similarity"):
    try:
        similarity = model.similarity(word1, word2)
        st.success(f"Similarity Score: {similarity:.3f}")
    except KeyError:
        st.error("❌ One or both words are not in the vocabulary. Try different words.")
