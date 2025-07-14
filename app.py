import wikipediaapi
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
            wiki_wiki = wikipediaapi.Wikipedia('de')
            page = wiki_wiki.page(begriff)
            if page.exists() and page.summary:
                technische_definition = page.summary.split(".")[0] + "."
            else:
                technische_definition = "Keine technische Definition bei Wikipedia gefunden."

        with st.spinner("KI denkt sich eine Metapher aus..."):
            prompt = f"""Erkläre den Begriff '{begriff}' mit einer klaren, einprägsamen Metapher oder Analogie aus dem Alltag, die jeder versteht. Die Erklärung soll nicht ausschweifend oder blumig sein, sondern das Wesentliche in einfacher Sprache treffen – maximal 3 Sätze, keine Fachbegriffe. Kein Geschwafel, sondern eine anschauliche, leicht merkbare Analogie."""
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

