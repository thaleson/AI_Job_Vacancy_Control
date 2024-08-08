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

      # Badges
    st.markdown(
        """
        <div style="display: flex; justify-content: space-between;">
            <div>
                <a href="https://github.com/thaleson" target="_blank">
                    <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" width="100" />
                </a>
            </div>
            <div>
                <a href="https://www.linkedin.com/in/thaleson-silva-9298a0296/" target="_blank">
                    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" width="100" />
                </a>
            </div>
            <div>
                <a href="mailto:thaleson177@gmail.com" target="_blank">
                    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" width="80" />
                </a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
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
