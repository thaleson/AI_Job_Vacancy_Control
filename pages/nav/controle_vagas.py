import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
import os

def run():
    st.title('Controle de Vagas de Emprego')

    def get_user_id():
        # Exemplo simples com uma entrada manual para o ID do usuário
        return st.text_input('Digite seu nome', 'seu nome')  # Substitua com sua lógica de autenticação

    def load_data(user_id):
        file_path = f'{user_id}_vagas.csv'
        if not os.path.exists(file_path):
            columns = ['ID', 'Data da Candidatura', 'Vaga', 'Nome da Empresa', 'Link da vaga',
                       'Origem da Candidatura', 'Pessoas da empresa adicionadas', 
                       'Linkedin da pessoa que mandei a mensagem', 'Ultimo contato pelo linkedin', 'Status']
            df = pd.DataFrame(columns=columns)
            df.to_csv(file_path, index=False)
        return pd.read_csv(file_path)

    def save_data(df, user_id):
        df.to_csv(f'{user_id}_vagas.csv', index=False)

    def prepare_features(data):
        le_status = LabelEncoder()
        data['Status_encoded'] = le_status.fit_transform(data['Status'])

        try:
            data['Data da Candidatura'] = pd.to_datetime(data['Data da Candidatura'], format='%Y-%m-%d', errors='coerce')
            data = data.dropna(subset=['Data da Candidatura'])
            data['Data da Candidatura'] = data['Data da Candidatura'].map(datetime.toordinal)
        except Exception as e:
            st.error(f"Erro ao converter datas: {e}")
            return None, None, None, None

        X = data[['Data da Candidatura', 'Vaga', 'Nome da Empresa', 'Link da vaga',
                  'Origem da Candidatura', 'Pessoas da empresa adicionadas',
                  'Linkedin da pessoa que mandei a mensagem', 'Ultimo contato pelo linkedin']]
        y = data['Status_encoded']
        
        X = pd.get_dummies(X, drop_first=True)
        X_columns = X.columns
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        return X, y, scaler, X_columns

    def train_model(data):
        X, y, scaler, X_columns = prepare_features(data)
        
        if X is None or y is None:
            return None, None, None
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        scores = cross_val_score(model, X, y, cv=5)
        st.write(f"Acurácia média do modelo: {scores.mean():.2f}")
        
        return model, scaler, X_columns

    def predict(model, scaler, X_columns):
        data_hoje = st.date_input('Data da Candidatura para Previsão', datetime.today())
        vaga_previsao = st.text_input('Vaga para Previsão')
        nome_empresa_previsao = st.text_input('Nome da Empresa para Previsão')
        link_vaga_previsao = st.text_input('Link da Vaga para Previsão')
        origem_candidatura_previsao = st.text_input('Origem da Candidatura para Previsão')
        pessoas_adicionadas_previsao = st.text_input('Pessoas da empresa adicionadas para Previsão')
        linkedin_mensagem_previsao = st.text_input('Linkedin da pessoa que mandei a mensagem para Previsão')
        ultimo_contato_previsao = st.text_input('Último contato pelo linkedin para Previsão')

        if st.button('Prever'):
            if not (vaga_previsao and nome_empresa_previsao and link_vaga_previsao and origem_candidatura_previsao and pessoas_adicionadas_previsao and linkedin_mensagem_previsao and ultimo_contato_previsao):
                st.warning('Preencha todos os dados para análise e previsão do modelo')
            else:
                data_hoje_ordinal = datetime.toordinal(data_hoje)
                input_features = pd.DataFrame([[data_hoje_ordinal, vaga_previsao, nome_empresa_previsao, link_vaga_previsao,
                                                origem_candidatura_previsao, pessoas_adicionadas_previsao,
                                                linkedin_mensagem_previsao, ultimo_contato_previsao]],
                                              columns=['Data da Candidatura', 'Vaga', 'Nome da Empresa', 'Link da vaga',
                                                       'Origem da Candidatura', 'Pessoas da empresa adicionadas',
                                                       'Linkedin da pessoa que mandei a mensagem', 'Ultimo contato pelo linkedin'])
                
                input_features = pd.get_dummies(input_features, drop_first=True)
                input_features = input_features.reindex(columns=X_columns, fill_value=0)
                input_features = scaler.transform(input_features)
                
                probabilidade = model.predict_proba(input_features)
                
                if probabilidade.shape[1] > 1:
                    probabilidade = probabilidade[0][1]  # Probabilidade de ser classificado como 'Status positivo'
                else:
                    probabilidade = probabilidade[0][0]  # Caso haja apenas uma classe
                
                if probabilidade > 0.50:
                    st.success(f"Você tem {probabilidade * 100:.2f}% de chance de sucesso. Resultado: Sucesso")
                else:
                    st.warning(f"Você tem {probabilidade * 100:.2f}% de chance de sucesso. Resultado: Não desista")

    st.subheader('Adicionar Nova Vaga')
    user_id = get_user_id()
    if not user_id:
        st.warning('Por favor, insira um ID de usuário para continuar.')
        return

    df = load_data(user_id)

    with st.form(key='add_vaga_form'):
        vaga = st.text_input('Vaga')
        nome_empresa = st.text_input('Nome da Empresa')
        link_vaga = st.text_input('Link da Vaga')
        origem_candidatura = st.text_input('Origem da Candidatura')
        pessoas_adicionadas = st.text_input('Pessoas da empresa adicionadas')
        linkedin_mensagem = st.text_input('Linkedin da pessoa que mandei a mensagem')
        ultimo_contato = st.text_input('Último contato pelo linkedin')
        status = st.selectbox('Status', ['Em Processo', 'Sem Retorno', 'Com Retorno'])
        data_candidatura = st.date_input('Data da Candidatura')

        submit_button = st.form_submit_button(label='Adicionar Vaga')
        if submit_button:
            if not (vaga and nome_empresa and link_vaga and origem_candidatura and pessoas_adicionadas and linkedin_mensagem and ultimo_contato and status and data_candidatura):
                st.warning('Preencha todos os dados por favor')
            else:
                new_data = pd.DataFrame({
                    'ID': [len(df) + 1],
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

    st.subheader('Excluir Vaga')
    vagas = df['ID'].tolist()
    vaga_para_deletar = st.selectbox('Selecione a vaga para excluir', vagas)
    if st.button('Excluir Vaga'):
        if vaga_para_deletar:
            df = df[df['ID'] != vaga_para_deletar]
            save_data(df, user_id)
            st.success('Vaga excluída com sucesso!')

    st.subheader('Dados das Vagas')
    st.dataframe(df)

    st.subheader('Gráficos de Vagas')
    if len(df) > 0:
        df['Data da Candidatura'] = pd.to_datetime(df['Data da Candidatura'], errors='coerce')
        df = df.dropna(subset=['Data da Candidatura'])
        
        fig, ax = plt.subplots()
        df['Quantidade'] = 1
        df.groupby(df['Data da Candidatura'].dt.to_period('M')).sum()['Quantidade'].plot(ax=ax)
        ax.set_title('Quantidade de Vagas por Mês')
        ax.set_xlabel('Mês')
        ax.set_ylabel('Quantidade')
        st.pyplot(fig)

    st.subheader('Treinamento do Modelo')
    if st.button('Treinar Modelo'):
        model, scaler, X_columns = train_model(df)
        if model:
            st.success('Modelo treinado com sucesso!')
        else:
            st.error('Erro ao treinar o modelo.')

    if model:
        st.subheader('Previsão de Vaga')
        predict(model, scaler, X_columns)

if __name__ == '__main__':
    run()
