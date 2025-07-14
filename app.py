import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# API-Key aus .env laden (lokal)
load_dotenv()
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Erklärungsgenerator", page_icon="📘")
st.title("🧠 Zwei Perspektiven auf Tech-Begriffe")
st.write("Gib einen Tech-Begriff ein und bekomme eine technische Definition sowie einen bildhaften, kreativen Vergleich.")

begriff = st.text_input("🔤 Begriff eingeben:")

if st.button("Erklären"):
    if begriff:
        with st.spinner("Denke nach..."):
            prompt = f"""Erkläre den Begriff '{begriff}' in genau zwei Abschnitten:

1. Technische Definition: Eine sachliche, technische Definition in einem Satz (ohne Beispiele).
2. Alltagsmetapher: Erkläre den Begriff mit einer bildhaften, gerne auch etwas ausführlicheren Metapher oder einem Vergleich aus dem Alltag. Schreibe eine kleine, verständliche Alltagsgeschichte, die den Begriff leicht greifbar macht. Nutze dabei keine Fachbegriffe, sondern anschauliche und emotionale Sprache.

Antworte genau in diesem Format und beginne den zweiten Abschnitt nach 'Alltagsmetapher:' in einer neuen Zeile.
"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )

            antwort = response.choices[0].message.content

            # Aufteilung und Darstellung in zwei Spalten:
            teile = antwort.split("Alltagsmetapher:")
            if len(teile) == 2:
                technische_definition = teile[0].replace("Technische Definition:", "").replace("1.", "").strip()
                alltagsmetapher = teile[1].strip()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### 💡 Technische Definition")
                    st.info(technische_definition)
                with col2:
                    st.markdown("### 🌈 Alltagsmetapher")
                    st.success(alltagsmetapher)
            else:
                st.write(antwort)
    else:
        st.warning("Bitte gib einen Begriff ein.")
