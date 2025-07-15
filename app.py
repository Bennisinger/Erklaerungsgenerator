import wikipedia
import streamlit as st
from openai import OpenAI

# API-Key für Deployment
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Farben
BACKGROUND = "#F7D6B3"
TECH_BOX = "#ECE6F3"
META_BOX = "#FFF7E0"
DARK = "#29223D"

st.set_page_config(page_title="Erklärungs-Generator", page_icon="💡", layout="centered")

# Setze Hintergrundfarbe mit CSS
st.markdown(
    f"""
    <style>
        body {{
            background-color: {BACKGROUND} !important;
        }}
        .block-container {{
            background-color: {BACKGROUND} !important;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Neuer Titel, ohne Emoji
st.markdown(
    f"""
    <h1 style="color:{DARK}; font-size:2.3em; margin-bottom:0;">
        Erklärungs-Generator: Aus Technisch wird Metaphorisch
    </h1>
    """, unsafe_allow_html=True
)

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

        st.markdown("---")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"""
                <div style="background-color: {TECH_BOX}; border-radius: 18px; padding: 20px; margin-bottom: 12px; box-shadow: 0 2px 8px #b6e0fe55;">
                <h3 style="margin-top:0; color:{DARK};">🛠️ Technische Definition (Wikipedia)</h3>
                <div style="font-size: 1.1em; color:{DARK};">{technische_definition}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"""
                <div style="background-color: {META_BOX}; border-radius: 18px; padding: 20px; margin-bottom: 12px; box-shadow: 0 2px 8px #dde9d1aa;">
                <h3 style="margin-top:0; color:{DARK};">📸 Metaphorisch</h3>
                <div style="font-size: 1.1em; color:{DARK};">{alltagsmetapher}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.warning("Bitte gib einen Begriff ein.")
