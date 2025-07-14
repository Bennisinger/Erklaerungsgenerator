import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# API-Key aus .env laden
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# App-Layout
st.set_page_config(page_title="Erklärungsgenerator", page_icon="📘")
st.title("🔍 Erklärungsgenerator für Tech-Begriffe")
st.write("Gib einen technischen Begriff ein, und ich erkläre ihn dir einfach, bildhaft und verständlich.")

# Eingabefeld
begriff = st.text_input("🔤 Begriff eingeben:")

# Wenn Button gedrückt wird
if st.button("Erklären"):
    if begriff:
        with st.spinner("Denke nach..."):
            prompt = f"Erkläre den Begriff '{begriff}' so, dass ihn ein neugieriger Mensch ohne Technik-Vorkenntnisse versteht. Nutze eine einfache, bildhafte Metapher und ein kurzes Beispiel aus dem Alltag. Die Erklärung soll so verständlich sein, dass sie im Kopf bleibt – wie eine gute Geschichte."

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            antwort = response.choices[0].message.content
            st.markdown("### 🧠 Erklärung:")
            st.write(antwort)
    else:
        st.warning("Bitte gib einen Begriff ein.")
