import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

def run():
    """
    Função principal que executa a aplicação Streamlit para controle de vagas de emprego.
    Inclui funcionalidades para adicionar, excluir e visualizar vagas, além de treinar e
    realizar previsões com um modelo de Machine Learning.
    """
    
    st.title('Controle de Vagas de Emprego')

    def get_user_id():
        """
        Solicita ao usuário que insira seu nome para criar um identificador único.
        
        Returns:
            str: Nome do usuário, utilizado como ID para o arquivo CSV.
        """
        return st.text_input('Digite seu nome', 'seu nome')

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
            if not (id_vaga and data_candidatura and vaga and nome_empresa and link_vaga and origem_candidatura and pessoas_adicionadas and linkedin_mensagem and ultimo_contato):
                st.warning('Por favor, preencha todos os campos.')
            else:
                try:
                    data_candidatura = datetime.strptime(str(data_candidatura), '%Y-%m-%d')
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
                except ValueError:
                    st.error('Erro ao converter a data. Verifique o formato da data inserida.')

    st.subheader('Visualizar Vagas')
    if st.button('Mostrar Vagas'):
        st.write(df)


if __name__ == "__main__":
    run()
