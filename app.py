import wikipedia
import streamlit as st
from openai import OpenAI

# API-Key für Deployment
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Erklärungsgenerator", page_icon="💡")
st.title("💡 Tech-Begriff erklärt: Wikipedia + KI-Metapher")

begriff = st.text_input("🔤 Begriff eingeben:")

if st.button("Erklären"):
    if begriff:
        with st.spinner("Hole technische Definition von Wikipedia..."):
            wikipedia.set_lang("de")
            try:
                technische_definition = wikipedia.summary(begriff, sentences=1, auto_suggest=False, redirect=True)
            except Exception:
                technische_definition = "Keine technische Definition bei Wikipedia gefunden."

        with st.spinner("KI denkt sich eine Metapher aus..."):
            prompt = f"""Erkläre den Begriff '{begriff}' mit einer einzigen, einprägsamen Metapher oder Analogie aus dem Alltag, die wirklich im Kopf bleibt. Nutze KEINE Umschreibungen und keine doppelte Vergleiche. Fasse dich auf maximal 2–3 Sätze, verwende eine einfache, anschauliche Alltagssituation oder einen Gegenstand, sodass jeder sofort ein Bild im Kopf hat. Kein Fachvokabular, kein Lehrbuchstil. Beispiel für einen guten Stil: 'Machine Learning ist wie das Training eines Hundes.'"""
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            alltagsmetapher = response.choices[0].message.content.strip()

        # Zwei Spalten für die Ausgabe
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 💡 Technische Definition (Wikipedia)")
            st.info(technische_definition)
        with col2:
            st.markdown("### 🌈 Metapher/Analogie")
            st.success(alltagsmetapher)
    else:
        st.warning("Bitte gib einen Begriff ein.")
