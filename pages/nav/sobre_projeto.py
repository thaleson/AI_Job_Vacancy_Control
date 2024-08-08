import streamlit as st

def run():
    st.title('Sobre o Projeto')
    
    st.subheader('Descrição do Projeto')
    st.write("""
        Este projeto é uma aplicação web destinada a ajudar você a gerenciar e analisar suas candidaturas a empregos. 
        A plataforma permite adicionar novas vagas, visualizar o progresso das candidaturas e realizar previsões sobre suas chances de sucesso.
    """)
    
    st.subheader('Objetivos')
    st.write("""
        - **Gerenciar Candidaturas**: Adicione, visualize e exclua informações sobre suas candidaturas a empregos.
        - **Analisar Dados**: Obtenha insights sobre o progresso das suas aplicações e o histórico de vagas.
        - **Sugestões de Melhoria**: Receba recomendações para aumentar suas chances de ser chamado para uma entrevista.
    """)
    
    st.subheader('Previsões e Análises com IA')
    st.write("""
        O projeto utiliza técnicas de aprendizado de máquina para prever a probabilidade de sucesso em suas candidaturas. As previsões são baseadas em dados históricos e nas informações das vagas que você adiciona. A plataforma permite:
        
        - **Análise Preditiva**: Algoritmos de machine learning avaliam suas chances de ser chamado para uma entrevista com base no perfil das vagas e no progresso das suas candidaturas.
        - **Sugestões Personalizadas**: Receba conselhos específicos para melhorar suas chances de sucesso nas candidaturas, ajustados ao seu perfil e ao tipo de vaga.
        - **Integração de Dados**: Futuras melhorias incluirão a integração com outras fontes de dados para oferecer análises ainda mais precisas e detalhadas.
    """)

    st.subheader('Uso do CSV')
    st.write("""
        O projeto utiliza um arquivo CSV para armazenar todas as informações sobre suas candidaturas. O CSV contém colunas para:
        - Nome da Empresa
        - Localização
        - Link da Vaga
        - Progresso
        - Data da Aplicação
        - Tipo de Vaga
        - Setor
        
        O arquivo CSV é a base para análise e previsões. Com ele, o sistema pode:
        - **Adicionar e Excluir Dados**: Inclua novas candidaturas ou remova informações desatualizadas.
        - **Analisar o Histórico**: Visualize gráficos e análises baseados nos dados armazenados.
        - **Treinar Modelos**: Dados suficientes permitem treinar modelos preditivos para oferecer insights mais precisos.
    """)
    
    st.subheader('Considerações Finais')
    st.write("""
        O projeto é uma ferramenta em evolução, e estamos constantemente aprimorando suas funcionalidades com base no feedback dos usuários. Agradecemos seu interesse e estamos abertos a sugestões para tornar a aplicação ainda mais útil.
    """)
