import streamlit as st
import gdown
import os
import time
import random
from gensim.models import KeyedVectors

# File settings
# File and Google Drive settings
MODEL_PATH = "frmodel.bin"
GOOGLE_DRIVE_ID = "1LREFqIB3mVKOdozoJDhnHxVirIi4EhTl"  # Replace with your actual file ID

# 🔹 Function to download the model correctly
def download_model():
    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 5000000:  # Ensure file isn't too small
        st.info("📥 Chargement du modèle...")
        url = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        st.success("✅ Model chargé!")

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
st.title("🔍 Akinamot")

# User inputs (converted to lowercase)
word1 = st.text_input("🔤 Premier mot:").strip().lower()
word2 = st.text_input("🔤 Deuxième mot:").strip().lower()
THRESHOLD = 0.215  # The similarity threshold

# Button to check similarity
if st.button("🔍 Sont-ils proches ?"):
    if word1 and word2:
        try:
            similarity = model.similarity(word1, word2)

            # 🔥 Flickering Effect (Roulette)
            st.markdown("### 🎡 Validation...")
            result_placeholder = st.empty()

            flicker_choices = [
                ("✅ OUI", "#34D399"),  # Green (YES)
                ("❌ NON", "#EF4444"),  # Red (NO)
            ]

            for _ in range(25):  # Flicker for ~5 seconds (0.2s per frame)
                text, color = random.choice(flicker_choices)
                result_placeholder.markdown(
                    f"""
                    <div style='background-color: {color}; padding: 20px; text-align: center; font-size: 32px; color: white; font-weight: bold; margin-top: 10px;'>
                        {text}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                time.sleep(0.2)

            # ✅ Final Decision
            final_result = "✅ OUI" if similarity > THRESHOLD else "❌ NON"
            final_color = "#34D399" if similarity > THRESHOLD else "#EF4444"

            result_placeholder.markdown(
                f"""
                <div style='background-color: {final_color}; padding: 20px; text-align: center; font-size: 40px; color: white; font-weight: bold; margin-top: 10px;'>
                    {final_result}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Display similarity score
            st.info(f"**Similarity Score:** `{similarity:.3f}` (Threshold: {THRESHOLD})")
        except KeyError:
            st.error("❌ Un ou des mots n'ont pas été trouvés")
    else:
        st.warning("⚠️ Champs vides")