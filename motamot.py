import streamlit as st
import gdown
import os
import time
import random
from gensim.models import KeyedVectors

# File settings
MODEL_PATH = "frmodel.bin"
GOOGLE_DRIVE_ID = "1LREFqIB3mVKOdozoJDhnHxVirIi4EhTl"  # Replace with your actual file ID

# 🔹 Function to download the model correctly
def download_model():
    msg = st.empty() 

    if not os.path.exists(MODEL_PATH) or os.path.getsize(MODEL_PATH) < 5000000:
        msg.info("📥 Chargement du modèle...")
        url = f"https://drive.google.com/uc?id={GOOGLE_DRIVE_ID}"
        gdown.download(url, MODEL_PATH, quiet=False)
        msg.success("✅ Modèle chargé!")

        time.sleep(1.5) 

    msg.empty() 

# 🔹 Load model with proper format
@st.cache_resource
def load_model():
    download_model()  # Ensure model is downloaded
    try:
        model = KeyedVectors.load_word2vec_format(MODEL_PATH, binary=True)  # Correct way for .bin models
        return model
    except Exception as e:
        st.error(f"❌ Échec du chargement du modèle: {e}")
        st.stop()

# 🔹 Load model
model = load_model()

# 🔹 Streamlit UI
st.title("🔍 Akinamot")

col1, col2 = st.columns([1, 3])

with col1:
    st.image("mascotte.png")

with col2:
    st.markdown(
        "<div style='color: white; font-weight: bold; font-size: 20px;'>"
        "Bienvenue sur Akinamot !<br>Je suis là pour vous aider à comparer deux mots."
        "</div>",
        unsafe_allow_html=True
    )

# User inputs (converted to lowercase)
word1 = st.text_input("🔤 Premier mot:").strip().lower()
word2 = st.text_input("🔤 Deuxième mot:").strip().lower()
THRESHOLD = 0.215  # The similarity threshold

# Button to check similarity
if st.button("🔍 Sont-ils proches ?"):
    if word1 and word2:
        try:
            similarity = model.similarity(word1, word2)

            # **Placeholder for validation message (will disappear)**
            validation_message = st.empty()
            validation_message.markdown("### 🎡 Validation en cours...")

            # **Placeholder for flickering effect**
            result_placeholder = st.empty()

            flicker_choices = [
                ("✅ OUI", "#34D399"),  # Green (YES)
                ("❌ NON", "#EF4444"),  # Red (NO)
            ]

            # CSS Animation for smooth effect (0.4s duration)
            st.markdown(
                """
                <style>
                @keyframes fadeInOut {
                    0% { opacity: 1; }
                    50% { opacity: 0.2; }
                    100% { opacity: 1; }
                }
                .flicker {
                    animation: fadeInOut 0.4s infinite alternate;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            start_time = time.time()
            while time.time() - start_time < 5:  # Ensures animation runs for 5 seconds
                text, color = random.choice(flicker_choices)
                result_placeholder.markdown(
                    f"""
                    <div class='flicker' style='background-color: {color}; padding: 25px; text-align: center; font-size: 36px; color: white; font-weight: bold; margin-top: 10px;'>
                        {text}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                time.sleep(0.2)  # Slower flickering (0.4s per switch)

            # **Remove the validation message after animation**
            validation_message.empty()

            # ✅ Final Decision
            final_result = "✅ OUI" if similarity > THRESHOLD else "❌ NON"
            final_color = "#34D399" if similarity > THRESHOLD else "#EF4444"

            # Display final result
            result_placeholder.markdown(
                f"""
                <div style='background-color: {final_color}; padding: 25px; text-align: center; font-size: 42px; color: white; font-weight: bold; margin-top: 10px;'>
                    {final_result}
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Display similarity score
            st.info(f"**Score de Similarité:** `{similarity:.3f}` (Seuil: {THRESHOLD})")
        except KeyError:
            st.error("❌ Un ou des mots n'ont pas été trouvés")
    else:
        st.warning("⚠️ Champs vides")
