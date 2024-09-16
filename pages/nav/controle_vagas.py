import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import uuid  # Para gerar IDs únicos

def run():
    st.title('Controle de Vagas de Emprego')

    def get_user_id():
        return st.text_input('Digite seu nome', 'seu nome')

    def load_data(user_id):
        file_path = f'{user_id}_vagas.csv'
        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=['ID', 'Data da Candidatura', 'Vaga', 'Nome da Empresa', 'Link da vaga', 'Origem da Candidatura', 'Pessoas da empresa adicionadas', 'Linkedin da pessoa que mandei a mensagem', 'Ultimo contato pelo linkedin', 'Status'])
            df.to_csv(file_path, index=False)
        return pd.read_csv(file_path)

    def save_data(df, user_id):
        df.to_csv(f'{user_id}_vagas.csv', index=False)

    def add_vaga(df):
        with st.form(key='add_vaga_form'):
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
                if not (data_candidatura and vaga and nome_empresa and link_vaga and origem_candidatura and pessoas_adicionadas and linkedin_mensagem and ultimo_contato):
                    st.warning('Por favor, preencha todos os campos.')
                else:
                    try:
                        # Gera um ID único
                        id_vaga = str(uuid.uuid4())
                        data_candidatura = datetime.strptime(str(data_candidatura), '%Y-%m-%d')
                        
                        # Adiciona a nova vaga ao DataFrame
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

    def excluir_vaga(df, user_id):
        st.subheader('Excluir Vaga')
        id_excluir = st.text_input('Digite o ID da vaga que deseja excluir:')
        if st.button('Excluir'):
            if id_excluir in df['ID'].values:
                df = df[df['ID'] != id_excluir]
                save_data(df, user_id)
                st.success(f'Vaga com ID {id_excluir} excluída com sucesso!')
            else:
                st.warning('ID não encontrado.')

    def resetar_csv(user_id):
        if st.button('Resetar CSV'):
            os.remove(f'{user_id}_vagas.csv')
            st.success('Arquivo CSV resetado com sucesso!')

    def gerar_graficos(df):
        st.subheader('Gráficos Detalhados')

        # Gráfico 1: Número de candidaturas ao longo do tempo
        df['Data da Candidatura'] = pd.to_datetime(df['Data da Candidatura'], errors='coerce')
        df_time = df['Data da Candidatura'].value_counts().sort_index()
        plt.figure(figsize=(10, 5))
        plt.plot(df_time.index, df_time.values, marker='o')
        plt.xlabel('Data da Candidatura')
        plt.ylabel('Número de Candidaturas')
        plt.title('Número de Candidaturas ao Longo do Tempo')
        st.pyplot(plt)

        # Gráfico 2: Origem das candidaturas
        df_origem = df['Origem da Candidatura'].value_counts()
        plt.figure(figsize=(8, 4))
        df_origem.plot(kind='bar')
        plt.xlabel('Origem da Candidatura')
        plt.ylabel('Quantidade')
        plt.title('Origem das Candidaturas')
        st.pyplot(plt)

        # Gráfico 3: Status das vagas
        df_status = df['Status'].value_counts()
        plt.figure(figsize=(8, 4))
        df_status.plot(kind='pie', autopct='%1.1f%%')
        plt.title('Status das Vagas')
        st.pyplot(plt)

    st.subheader('Adicionar Nova Vaga')
    user_id = get_user_id()
    if not user_id:
        st.warning('Por favor, insira um ID de usuário para continuar.')
        return

    df = load_data(user_id)
    add_vaga(df)
    excluir_vaga(df, user_id)
    resetar_csv(user_id)

    st.subheader('Visualizar Vagas')
    if st.button('Mostrar Vagas'):
        st.write(df)

    gerar_graficos(df)

if __name__ == "__main__":
    run()
