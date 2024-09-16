import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os
import uuid
import matplotlib.dates as mdates

def run():
    st.title('Controle de Vagas de Emprego')

    def get_user_id():
        return st.text_input('Digite seu nome', '')

    def load_data(user_id):
        file_path = f'{user_id}_vagas.csv'
        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=['ID', 'Data da Candidatura', 'Vaga', 'Nome da Empresa', 'Link da vaga',
                                       'Origem da Candidatura', 'Pessoas da empresa adicionadas',
                                       'Linkedin da pessoa que mandei a mensagem', 'Ultimo contato pelo linkedin', 'Status'])
            df.to_csv(file_path, index=False)
        return pd.read_csv(file_path)

    def save_data(df, user_id):
        df.to_csv(f'{user_id}_vagas.csv', index=False)

    def gerar_graficos(df):
        # Gráfico 1: Contagem de vagas por status
        if not df.empty:
            st.subheader('Gráfico de Status das Vagas')
            try:
                df_status = df['Status'].value_counts()
                st.bar_chart(df_status)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de status: {e}")

            # Gráfico 2: Contagem de origem das candidaturas
            st.subheader('Gráfico de Origem das Candidaturas')
            try:
                df_origem = df['Origem da Candidatura'].value_counts()
                st.bar_chart(df_origem)
            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de origem: {e}")

            # Gráfico 3: Candidaturas ao longo do tempo com visual mais detalhado
            st.subheader('Candidaturas ao Longo do Tempo')
            try:
                # Converter para datetime
                df['Data da Candidatura'] = pd.to_datetime(df['Data da Candidatura'], errors='coerce')
                df_tempo = df.set_index('Data da Candidatura').resample('M').size()

                # Criando um gráfico mais detalhado com matplotlib
                fig, ax = plt.subplots()
                ax.plot(df_tempo.index, df_tempo.values, marker='o', linestyle='-', color='b', label='Candidaturas')
                ax.set_title('Candidaturas ao Longo do Tempo', fontsize=16)
                ax.set_xlabel('Data', fontsize=14)
                ax.set_ylabel('Número de Candidaturas', fontsize=14)
                ax.legend()
                ax.grid(True)

                # Formatando as datas no eixo X
                ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
                fig.autofmt_xdate()

                # Ajustar limites do eixo Y
                ax.set_ylim(bottom=0)

                # Exibir o gráfico no Streamlit
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Erro ao gerar o gráfico de candidaturas ao longo do tempo: {e}")

    def excluir_vaga(df, user_id):
        st.subheader('Excluir Vaga')
        vaga_id = st.text_input('Digite o ID da vaga que deseja excluir:')
        if st.button('Excluir Vaga'):
            if vaga_id in df['ID'].values:
                df = df[df['ID'] != vaga_id]
                save_data(df, user_id)
                st.success('Vaga excluída com sucesso!')
            else:
                st.error('ID da vaga não encontrado.')
        return df

    st.subheader('Adicionar Nova Vaga')
    user_id = get_user_id()
    if not user_id:
        st.warning('Por favor, insira o nome  de usuário para continuar, se não tiver adicioner para continuar.')
        return

    df = load_data(user_id)

    with st.form(key='add_vaga_form'):
        id_vaga = str(uuid.uuid4())  # Gera um ID único
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
                    
                    # Garantir IDs únicos
                    if id_vaga in df['ID'].values:
                        st.error('Erro: ID duplicado encontrado. Tente novamente.')
                    else:
                        df = pd.concat([df, new_data], ignore_index=True)
                        save_data(df, user_id)
                        st.success('Vaga adicionada com sucesso!')
                except ValueError:
                    st.error('Erro ao converter a data. Verifique o formato da data inserida.')

    st.subheader('Visualizar Vagas')
    if st.button('Mostrar Vagas'):
        st.write(df)

    # Exclusão de vagas
    df = excluir_vaga(df, user_id)

    # Gráficos detalhados apenas se o nome do usuário for fornecido e houver dados
    if not df.empty:
        st.subheader('Gráficos Detalhados')
        gerar_graficos(df)

if __name__ == "__main__":
    run()
