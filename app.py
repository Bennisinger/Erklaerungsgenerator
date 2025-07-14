import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# API-Key aus .env laden (lokal)
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="Erklärungsgenerator", page_icon="📘")
st.title("🧠 Zwei Perspektiven auf Tech-Begriffe")
st.write("Gib einen Tech-Begriff ein und bekomme eine technische Definition sowie einen bildhaften, kreativen Vergleich.")

begriff = st.text_input("🔤 Begriff eingeben:")

if st.button("Erklären"):
    if begriff:
        with st.spinner("Denke nach..."):
            prompt = f"""Gib mir zwei kurze Erklärungen zum Begriff '{begriff}':
1. Eine sachliche, technische Definition in einem Satz (ohne Beispiele).
2. Eine bildhafte, gerne unterhaltsame und kreative Metapher oder einen Vergleich aus dem Alltag, der den Begriff für Laien verständlich macht. Die Erklärung darf 2–4 Sätze lang sein, anschaulich und mit einem Augenzwinkern geschrieben – aber ohne Fachbegriffe.
Antworte klar getrennt mit 'Technische Definition:' und 'Alltagsvergleich:'.
"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            antwort = response.choices[0].message.content
            st.markdown("### 🧑‍💻 Technische Definition & Alltagsvergleich:")
            st.write(antwort)
    else:
        st.warning("Bitte gib einen Begriff ein.")

