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
    Inclui funcionalidades para adicionar, excluir e visualizar vagas, além de gráficos
    para análise das candidaturas.
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

    def reset_data(user_id):
        """
        Reseta o arquivo CSV para um DataFrame vazio.

        Args:
            user_id (str): ID do usuário para determinar o nome do arquivo CSV.
        """
        file_path = f'{user_id}_vagas.csv'
        df = pd.DataFrame(columns=['ID', 'Data da Candidatura', 'Vaga', 'Nome da Empresa', 'Link da vaga', 'Origem da Candidatura', 'Pessoas da empresa adicionadas', 'Linkedin da pessoa que mandei a mensagem', 'Ultimo contato pelo linkedin', 'Status'])
        df.to_csv(file_path, index=False)
        st.success('Arquivo CSV resetado com sucesso!')

    st.subheader('Adicionar Nova Vaga')
    user_id = get_user_id()
    if not user_id:
        st.warning('Por favor, insira um ID de usuário para continuar.')
        return

    df = load_data(user_id)

    # Formulário para adicionar nova vaga
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

    # Excluir vaga por ID
    st.subheader('Excluir Vaga')
    vaga_id_to_delete = st.text_input('Digite o ID da vaga que deseja excluir')
    if st.button('Excluir Vaga'):
        if vaga_id_to_delete in df['ID'].values:
            df = df[df['ID'] != vaga_id_to_delete]
            save_data(df, user_id)
            st.success(f'Vaga com ID {vaga_id_to_delete} excluída com sucesso!')
        else:
            st.warning('ID da vaga não encontrado.')

    # Resetar o CSV
    st.subheader('Resetar Dados')
    if st.button('Resetar CSV'):
        reset_data(user_id)
        df = load_data(user_id)  # Recarrega o DataFrame após o reset

    # Visualizar Vagas
    st.subheader('Visualizar Vagas')
    if st.button('Mostrar Vagas'):
        st.write(df)

    # Gráficos
    st.subheader('Análise de Dados')

    # Gráfico de Candidaturas ao Longo do Tempo
    if not df.empty:
        df['Data da Candidatura'] = pd.to_datetime(df['Data da Candidatura'], errors='coerce')
        candidaturas_por_data = df.groupby(df['Data da Candidatura'].dt.to_period('M')).size()
        plt.figure(figsize=(10, 5))
        candidaturas_por_data.plot(kind='line', marker='o')
        plt.title('Candidaturas ao Longo do Tempo')
        plt.xlabel('Mês')
        plt.ylabel('Número de Candidaturas')
        plt.xticks(rotation=45)
        st.pyplot(plt)

        # Gráfico de Status das Vagas
        status_counts = df['Status'].value_counts()
        plt.figure(figsize=(10, 5))
        status_counts.plot(kind='bar')
        plt.title('Distribuição do Status das Vagas')
        plt.xlabel('Status')
        plt.ylabel('Quantidade')
        st.pyplot(plt)
    else:
        st.info('Nenhuma vaga cadastrada para gerar gráficos.')

if __name__ == "__main__":
    run()
