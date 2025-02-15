import streamlit as st
import os
from gensim.models import KeyedVectors

# 🔹 Load the model only once (better efficiency)
@st.cache_resource
def load_model():
    model_path = "frmodel.bin"  # Ensure your model is in the same directory
    if os.path.exists(model_path):
        return KeyedVectors.load(model_path)
    else:
        st.error("❌ Model file not found! Make sure 'frmodel.bin' is in the same directory.")
        return None

# Load model once
model = load_model()

# 🔹 Streamlit UI
st.title("🔍 Word2Vec Similarity Checker")

word1 = st.text_input("Enter first word:")
word2 = st.text_input("Enter second word:")

if st.button("Check Similarity"):
    if model:
        try:
            similarity = model.similarity(word1, word2)
            st.success(f"Similarity Score: {similarity:.3f}")
        except KeyError:
            st.error("❌ One or both words are not in the vocabulary. Try different words.")
    else:
        st.error("❌ Model not loaded. Please check your file location.")

