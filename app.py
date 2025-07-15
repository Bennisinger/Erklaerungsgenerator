import wikipedia
import streamlit as st
from openai import OpenAI

# API-Key für Deployment
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Farben
BACKGROUND = "#F7D6B3"
TECH_BOX = "#D7E8F7"
META_BOX = "#FFF7E0"
DARK = "#29223D"
LIGHTGREY = "#8A8A8A"

st.set_page_config(page_title="KI Erklärungs-Generator", page_icon="💡", layout="centered")

st.markdown(
    f"""
    <style>
        body {{
            background-color: {BACKGROUND} !important;
        }}
        .block-container {{
            background-color: {BACKGROUND} !important;
        }}
        .subtitle {{
            color: {DARK};
            font-size: 1.15em;
            margin-top: -8px;
            margin-bottom: 18px;
            font-weight: 400;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Titel und Untertitel mit Emojis
st.markdown(
    f"""
    <h1 style="color:{DARK}; font-size:2.3em; margin-bottom:0.2em;">
        KI Erklärungs-Generator
    </h1>
    <div class="subtitle">Von 🛠️ Technisch zu 📸 Metaphorisch</div>
    """, unsafe_allow_html=True
)

# --- Nebeneinander: Freie Eingabe und Dropdown ---
col1, col2 = st.columns([1.1, 1.1])

with col1:
    st.markdown("**KI-Fachbegriff eingeben:**")
    begriff = st.text_input("", key="inputfeld", label_visibility="collapsed")
    submit = st.button("Erklär's mir", key="erklaer_button")

with col2:
    st.markdown("**KI-Fachbegriff auswählen:**")
    dropdown_begriffe = [
        "Large Language Model",
        "Machine Learning",
        "Deep Learning",
        "Neuronales Netz",
        "Artificial General Intelligence",
        "Predictive Analytics",
        "Vektordatenbank",
        "Prompt Engineering",
        "Natural Language Processing",
        "Transfer Learning"
    ]
    selected_dropdown = st.selectbox(
        "",
        [""] + dropdown_begriffe,
        index=0,
        key="dropdown",
        label_visibility="collapsed"
    )

# --- Logik ---
trigger = False
if selected_dropdown:
    begriff = selected_dropdown
    trigger = True
elif submit and begriff:
    trigger = True

if trigger and begriff:
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

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            f"""
            <div style="background-color: {TECH_BOX}; border-radius: 18px; padding: 20px; margin-bottom: 12px; box-shadow: 0 2px 8px #b6e0fe55;">
            <h3 style="margin-top:0; color:{DARK};">🛠️ Technisch</h3>
            <div style="font-size: 1.1em; color:{DARK};">{technische_definition}</div>
            <div style="color:{LIGHTGREY}; font-size:0.95em; margin-top: 20px; text-align: right;">
                Quelle: Wikipedia (2025)
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div style="background-color: {META_BOX}; border-radius: 18px; padding: 20px; margin-bottom: 12px; box-shadow: 0 2px 8px #dde9d1aa;">
            <h3 style="margin-top:0; color:{DARK};">📸 Metaphorisch</h3>
            <div style="font-size: 1.1em; color:{DARK};">{alltagsmetapher}</div>
            </div>
            """,
            unsafe_allow_html=True
        )
elif submit and not begriff:
    st.warning("Bitte gib einen Begriff ein.")
