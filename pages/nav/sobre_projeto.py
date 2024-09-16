import streamlit as st

def run():
    st.title('Sobre o Projeto')
    
    st.subheader('Descrição do Projeto')
    st.write("""
        Este projeto é uma aplicação web desenvolvida para ajudar você a gerenciar e analisar suas candidaturas a empregos.
        A plataforma permite adicionar novas vagas, visualizar o progresso das candidaturas, analisar estatísticas e gráficos,
        além de excluir informações desatualizadas para manter seu controle sempre atualizado.
    """)
    
    st.subheader('Objetivos')
    st.write("""
        - **Gerenciar Candidaturas**: Adicione, visualize e exclua informações sobre suas candidaturas a empregos.
        - **Analisar Dados**: Obtenha insights sobre o progresso das suas aplicações e o histórico de vagas por meio de gráficos e estatísticas detalhadas.
        - **Visualizar Gráficos Detalhados**: Veja a distribuição de status das vagas, a origem das candidaturas e um gráfico de candidaturas ao longo do tempo.
        - **Exclusão de Vagas**: Remova candidaturas pelo ID, mantendo o controle de suas aplicações sempre atualizado.
    """)
    
    st.subheader('Previsões e Análises com IA')
    st.write("""
        O projeto está sendo preparado para incluir técnicas de aprendizado de máquina, que permitirão prever a probabilidade de sucesso em suas candidaturas.
        As previsões serão baseadas em dados históricos e nas informações das vagas que você adicionar. A plataforma permitirá:
        
        - **Análise Preditiva**: Algoritmos de machine learning poderão avaliar suas chances de ser chamado para uma entrevista com base no perfil das vagas e no progresso das suas candidaturas.
        - **Sugestões Personalizadas**: Em versões futuras, você poderá receber recomendações para melhorar suas chances de sucesso nas candidaturas, ajustadas ao seu perfil e ao tipo de vaga.
        - **Integração de Dados**: Futuras melhorias incluirão a integração com outras fontes de dados para oferecer análises ainda mais precisas e detalhadas.
    """)

    st.subheader('Uso do CSV')
    st.write("""
        O projeto utiliza um arquivo CSV para armazenar todas as informações sobre suas candidaturas. O CSV contém colunas para:
        - ID da Vaga (gerado automaticamente)
        - Data da Candidatura
        - Nome da Empresa
        - Vaga
        - Link da Vaga
        - Origem da Candidatura
        - Pessoas da empresa adicionadas
        - LinkedIn da pessoa que recebeu a mensagem
        - Último contato pelo LinkedIn
        - Status
        
        O arquivo CSV é a base para análise e previsões. Com ele, o sistema pode:
        - **Adicionar e Excluir Dados**: Inclua novas candidaturas ou remova informações desatualizadas diretamente pela aplicação.
        - **Visualizar Gráficos Detalhados**: Analise gráficos de status das vagas, origem das candidaturas e um gráfico de candidaturas ao longo do tempo.
        - **Treinar Modelos (Futuro)**: Dados suficientes permitirão treinar modelos preditivos para oferecer insights mais precisos.
    """)

    st.subheader('Gráficos e Análises')
    st.write("""
        - **Status das Vagas**: Um gráfico de barras exibe a distribuição dos status das candidaturas.
        - **Origem das Candidaturas**: Veja quais são as fontes mais frequentes das suas candidaturas.
        - **Candidaturas ao Longo do Tempo**: Um gráfico detalhado mostra a evolução das suas aplicações ao longo dos meses, ajudando a entender sua atividade de busca por empregos.
    """)

    st.subheader('Considerações Finais')
    st.write("""
        O projeto é uma ferramenta em constante evolução, e estamos aprimorando suas funcionalidades com base no feedback dos usuários.
        Sua opinião é fundamental para tornar a aplicação ainda mais útil e eficiente. Agradecemos seu interesse e estamos abertos a sugestões.
    """)

