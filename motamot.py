import streamlit as st
import gdown
import os
from gensim.models import KeyedVectors

# File settings
# File and Google Drive settings
MODEL_PATH = "frmodel.bin"
GOOGLE_DRIVE_ID = "1LREFqIB3mVKOdozoJDhnHxVirIi4EhTl"  # Replace with your actual file ID

# 🔹 Function to download the model correctly
def download_model():
    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 5000000:  # Ensure file isn't too small
        st.info("📥 Downloading Word2Vec model... (only happens once)")
        url = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        st.success("✅ Model downloaded successfully!")

# 🔹 Load model with proper format
@st.cache_resource
def load_model():
    download_model()  # Ensure model is downloaded
    try:
        model = KeyedVectors.load_word2vec_format(MODEL_PATH, binary=True)  # Correct way for .bin models
        return model
    except Exception as e:
        st.error(f"❌ Failed to load model: {e}")
        st.stop()

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
