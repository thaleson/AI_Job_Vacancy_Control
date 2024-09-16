import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def run():
    """
    Função principal que executa a aplicação Streamlit para controle de vagas de emprego.
    Inclui funcionalidades para adicionar, excluir e visualizar vagas, além de gráficos e recomendações.
    """
    st.title('Controle de Vagas de Emprego')

    def get_user_id():
        """
        Solicita ao usuário que insira seu nome para criar um identificador único.
        
        Returns:
            str: Nome do usuário, utilizado como ID para o arquivo CSV.
        """
        return st.text_input('Digite seu nome', 'seu_nome')

    def load_data(user_id):
        """
        Carrega os dados de um arquivo CSV com base no ID do usuário. Se o arquivo não existir,
        cria um novo DataFrame e salva como CSV.

        Args:
            user_id (str): ID do usuário para determinar o nome do arquivo CSV.

        Returns:
            pd.DataFrame: DataFrame carregado ou criado com as colunas padrão.
        """
        file_path = f'{user_id}_vagas.csv'
        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=['ID', 'Data da Candidatura', 'Vaga', 'Nome da Empresa', 'Link da vaga', 'Origem da Candidatura', 'Pessoas da empresa adicionadas', 'Linkedin da pessoa que mandei a mensagem', 'Ultimo contato pelo linkedin', 'Status'])
            df.to_csv(file_path, index=False)
        return pd.read_csv(file_path)

    def save_data(df, user_id):
        """
        Salva o DataFrame no arquivo CSV com base no ID do usuário.

        Args:
            df (pd.DataFrame): DataFrame a ser salvo.
            user_id (str): ID do usuário para determinar o nome do arquivo CSV.
        """
        df.to_csv(f'{user_id}_vagas.csv', index=False)

    def plot_status_distribution(df):
        """
        Plota um gráfico de barras mostrando a distribuição dos status das vagas.

        Args:
            df (pd.DataFrame): DataFrame com os dados das vagas.
        """
        st.subheader('Distribuição de Status das Vagas')
        status_counts = df['Status'].value_counts()
        fig, ax = plt.subplots()
        status_counts.plot(kind='bar', ax=ax)
        ax.set_title('Distribuição de Status')
        ax.set_xlabel('Status')
        ax.set_ylabel('Contagem')
        st.pyplot(fig)

    def plot_origin_distribution(df):
        """
        Plota um gráfico de barras mostrando a distribuição das origens das candidaturas.

        Args:
            df (pd.DataFrame): DataFrame com os dados das vagas.
        """
        st.subheader('Distribuição de Origem das Candidaturas')
        origin_counts = df['Origem da Candidatura'].value_counts()
        fig, ax = plt.subplots()
        origin_counts.plot(kind='bar', ax=ax)
        ax.set_title('Distribuição de Origem')
        ax.set_xlabel('Origem')
        ax.set_ylabel('Contagem')
        st.pyplot(fig)

    def recommend_best_vaga(df):
        """
        Recomenda a melhor vaga com base no status e na origem da candidatura.

        Args:
            df (pd.DataFrame): DataFrame com os dados das vagas.
        """
        st.subheader('Recomendação de Vaga')
        if not df.empty:
            # Critério de exemplo: vagas com status 'Entrevista' e origem 'LinkedIn'
            recomendada = df[(df['Status'] == 'Entrevista') & (df['Origem da Candidatura'] == 'LinkedIn')]
            if not recomendada.empty:
                st.write('Recomendação com base em vagas com status "Entrevista" e origem "LinkedIn":')
                st.write(recomendada[['ID', 'Vaga', 'Nome da Empresa']])
            else:
                st.write('Nenhuma vaga encontrada com os critérios selecionados.')
        else:
            st.write('Sem dados suficientes para recomendação.')

    st.subheader('Adicionar Nova Vaga')
    user_id = get_user_id()
    if not user_id:
        st.warning('Por favor, insira um ID de usuário para continuar.')
        return

    df = load_data(user_id)

    with st.form(key='add_vaga_form'):
        id_vaga = st.text_input('ID da Vaga')
        data_candidatura = st.date_input('Data da Candidatura')
        vaga = st.text_input('Vaga')
        nome_empresa = st.text_input('Nome da Empresa')
        link_vaga = st.text_input('Link da Vaga')
        origem_candidatura = st.text_input('Origem da Candidatura')
        pessoas_adicionadas = st.text_input('Pessoas da empresa adicionadas')
        linkedin_mensagem = st.text_input('Linkedin da pessoa que mandei a mensagem')
        ultimo_contato = st.text_input('Ultimo contato pelo linkedin')
        status = st.selectbox('Status', ['Aguardando', 'Entrevista', 'Rejeitado', 'Contratado'])
        
        submit_button = st.form_submit_button(label='Adicionar Vaga')
        if submit_button:
            if not (id_vaga and vaga and nome_empresa and origem_candidatura):
                st.warning('Por favor, preencha todos os campos obrigatórios.')
            else:
                # Evitar duplicatas
                if id_vaga in df['ID'].values:
                    st.warning('Vaga com esse ID já existe.')
                else:
                    try:
                        new_data = pd.DataFrame({
                            'ID': [id_vaga],
                            'Data da Candidatura': [data_candidatura],
                            'Vaga': [vaga],
                            'Nome da Empresa': [nome_empresa],
                            'Link da vaga': [link_vaga],
                            'Origem da Candidatura': [origem_candidatura],
                            'Pessoas da empresa adicionadas': [pessoas_adicionadas],
                            'Linkedin da pessoa que mandei a mensagem': [linkedin_mensagem],
                            'Ultimo contato pelo linkedin': [ultimo_contato],
                            'Status': [status]
                        })
                        df = pd.concat([df, new_data], ignore_index=True)
                        save_data(df, user_id)
                        st.success('Vaga adicionada com sucesso!')
                    except Exception as e:
                        st.error(f'Erro ao adicionar vaga: {e}')

    st.subheader('Visualizar Vagas')
    if st.button('Mostrar Vagas'):
        st.write(df)

    # Exibir gráficos
    if not df.empty:
        plot_status_distribution(df)
        plot_origin_distribution(df)
        recommend_best_vaga(df)

if __name__ == "__main__":
    run()
