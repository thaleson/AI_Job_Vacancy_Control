import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os
import io
from fpdf import FPDF

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

    # Função para exportar para Excel
    def export_to_excel(df):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Vagas')
        processed_data = output.getvalue()
        return processed_data

    # Função para exportar para PDF
    def export_to_pdf(df):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 12)
        for col_name in df.columns:
            pdf.cell(40, 10, col_name, 1, 0, 'C')
        pdf.ln()
        pdf.set_font('Arial', '', 12)
        for index, row in df.iterrows():
            for item in row:
                pdf.cell(40, 10, str(item), 1, 0, 'C')
            pdf.ln()
        output = io.BytesIO()
        pdf.output(output)
        return output.getvalue()

    # Outras funções...

    st.subheader('Adicionar Nova Vaga')
    user_id = get_user_id()
    if not user_id:
        st.warning('Por favor, insira um ID de usuário para continuar.')
        return

    df = load_data(user_id)

    # Formulário para adicionar vaga
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
            if not (id_vaga and data_candidatura and vaga and nome_empresa and link_vaga and origem_candidatura and pessoas_adicionadas and linkedin_mensagem and ultimo_contato and status):
                st.warning('Preencha todos os dados por favor')
            else:
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

    st.subheader('Exportar Dados')
    if len(df) > 0:
        export_excel = st.button('Exportar para Excel')
        export_pdf = st.button('Exportar para PDF')

        if export_excel:
            excel_data = export_to_excel(df)
            st.download_button(
                label='Baixar Excel',
                data=excel_data,
                file_name=f'{user_id}_vagas.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

        if export_pdf:
            pdf_data = export_to_pdf(df)
            st.download_button(
                label='Baixar PDF',
                data=pdf_data,
                file_name=f'{user_id}_vagas.pdf',
                mime='application/pdf'
            )

    # Restante do código...

if __name__ == "__main__":
    run()
