import streamlit as st
import json
from streamlit_lottie import st_lottie


def run():
    
    # Colunas que organizam a página
    col1, col2 = st.columns(2)

    # animações
    with open("assets/pagina_inicial1.json") as source:
        animacao_1 = json.load(source)

    with open("assets/animation1.json") as source:
        animacao_2 = json.load(source)
    
    # conteúdo a ser exibido na coluna 1
    with col1:
        st_lottie(animacao_1, height=350, width=400)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown("<h5 style='text-align: justify;'>   Oi the best mentora Mariana Vicentin Gallo (She/Her)  Conexão de 1º grau  Bilingual Tech Recruiter at Tateeda | Talent Acquisition | Headhunting | HRBP  Fiz esse projeto que você me pediu.</h5>", unsafe_allow_html=True)

    # conteúdo a ser exibido na coluna 2
    with col2:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown("<h5 style='text-align: justify;'> Bem-vindo ao Controle de Vagas de Emprego! 🎉</h5>", unsafe_allow_html=True)
        st_lottie(animacao_2, height=400, width=440)