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
            prompt = f"""Erkläre den Begriff '{begriff}' ausschließlich mit einer einzigen, klaren Metapher oder Analogie aus dem Alltag. Wähle dafür einen echten, greifbaren Gegenstand oder Vorgang (wie Tetris, Post-it, Werkzeugkasten, Baukasten, Puzzle, Bibliothek, ...), KEINE abstrakten Begriffe oder Umschreibungen. Verwende nicht das Wort selbst oder Ableitungen davon in der Erklärung. In maximal 3 Sätzen soll sofort ein konkretes, überraschendes Bild im Kopf entstehen, das den Kern des Begriffs einfängt. Beispiel für Stil: 'Machine Learning ist wie das Training eines Hundes.'"""
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
