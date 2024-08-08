import streamlit as st
from streamlit_option_menu import option_menu
import json
from streamlit_lottie import st_lottie

# Configuração da página
st.set_page_config(
    page_title='Controle de Vagas de Emprego',
    page_icon='📋',
    layout='wide'
)

# Aplicar estilos de CSS à página
with open("static/style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Função para carregar animação JSON
def load_lottie(file_path):
    with open(file_path, "r") as file:
        return json.load(file)

# Menu de navegação com ícones
with st.sidebar:
    st.title('Menu')
    option = option_menu(
        menu_title=None,  # Não mostrar título do menu
        options=['Home', 'Controle de Vagas de Emprego', 'Sobre o Projeto'],
        icons=['house', 'briefcase', 'info-circle'],  # Ícones correspondentes
        default_index=0,  # Página padrão
        orientation='vertical'
    )

# Redirecionar para a página correspondente
if option == 'Home':
    import pages.nav.home as home
    home.run()
elif option == 'Controle de Vagas de Emprego':
    import pages.nav.controle_vagas as controle_vagas
    controle_vagas.run()
elif option == 'Sobre o Projeto':
    import pages.nav.sobre_projeto as sobre_projeto
    sobre_projeto.run()
