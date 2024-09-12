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
        return st.text_input('Digite seu nome', 'seu nome')

    def load_data(user_id):
        file_path = f'{user_id}_vagas.csv'
        if not os.path.exists(file_path):
            df = pd.DataFrame(columns=[
                'ID', 'Data da Candidatura', 'Vaga', 'Nome da Empresa', 'Link da vaga',
                'Origem da Candidatura', 'Pessoas da empresa adicionadas', 
                'Linkedin da pessoa que mandei a mensagem', 'Último contato pelo linkedin', 'Status'
            ])
            df.to_csv(file_path, index=False)
        return pd.read_csv(file_path)

    def save_data(df, user_id):
        df.to_csv(f'{user_id}_vagas.csv', index=False)

    def prepare_features(data):
        le_status = LabelEncoder()
        data['Status_encoded'] = le_status.fit_transform(data['Status'])

        try:
            if 'Data da Candidatura' not in data.columns:
                st.error("Coluna 'Data da Candidatura' não encontrada no DataFrame.")
                return None, None, None, None

            data['Data da Candidatura'] = pd.to_datetime(data['Data da Candidatura'], format='%Y-%m-%d', errors='coerce')
            data = data.dropna(subset=['Data da Candidatura'])
            data['Data da Candidatura'] = data['Data da Candidatura'].map(datetime.toordinal)
        except Exception as e:
            st.error(f"Erro ao converter datas: {e}")
            return None, None, None, None

        X = data[['Data da Candidatura', 'Vaga', 'Origem da Candidatura', 'Pessoas da empresa adicionadas', 
                  'Linkedin da pessoa que mandei a mensagem', 'Último contato pelo linkedin']]
        y = data['Status_encoded']
        
        X = pd.get_dummies(X, columns=['Vaga', 'Origem da Candidatura', 'Pessoas da empresa adicionadas', 
                                        'Linkedin da pessoa que mandei a mensagem', 'Último contato pelo linkedin'], drop_first=True)
        X_columns = X.columns
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        return X, y, scaler, X_columns

    def train_model(data):
        X, y, scaler, X_columns = prepare_features(data)
        
        if X is None or y is None:
            return None, None, None
        
        if len(X) < 7:
            st.warning("Dados insuficientes para treinar o modelo. Por favor, adicione mais dados.")
            return None, None, None
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        scores = cross_val_score(model, X, y, cv=5)
        st.write(f"Acurácia média do modelo: {scores.mean():.2f}")
        
        return model, scaler, X_columns

    def predict(model, scaler, X_columns):
        data_candidatura = st.date_input('Data da Candidatura para Previsão', datetime.today())
        vaga_previsao = st.text_input('Vaga para Previsão')
        origem_candidatura = st.text_input('Origem da Candidatura')
        pessoas_adicionadas = st.text_input('Pessoas da empresa adicionadas')
        linkedin_pessoa = st.text_input('Linkedin da pessoa que mandei a mensagem')
        ultimo_contato = st.text_input('Último contato pelo linkedin')

        if st.button('Prever'):
            if not (vaga_previsao and origem_candidatura and pessoas_adicionadas and linkedin_pessoa and ultimo_contato):
                st.warning('Preencha todos os dados para análise e previsão do modelo')
            else:
                data_candidatura_ordinal = datetime.toordinal(data_candidatura)
                input_features = pd.DataFrame([[data_candidatura_ordinal, vaga_previsao, origem_candidatura, 
                                                pessoas_adicionadas, linkedin_pessoa, ultimo_contato]],
                                            columns=['Data da Candidatura', 'Vaga', 'Origem da Candidatura', 
                                                     'Pessoas da empresa adicionadas', 
                                                     'Linkedin da pessoa que mandei a mensagem', 
                                                     'Último contato pelo linkedin'])
                
                input_features = pd.get_dummies(input_features, columns=['Vaga', 'Origem da Candidatura', 
                                                                         'Pessoas da empresa adicionadas', 
                                                                         'Linkedin da pessoa que mandei a mensagem', 
                                                                         'Último contato pelo linkedin'], drop_first=True)
                input_features = input_features.reindex(columns=X_columns, fill_value=0)
                input_features = scaler.transform(input_features)
                
                probabilidade = model.predict_proba(input_features)
                
                if probabilidade.shape[1] > 1:
                    probabilidade = probabilidade[0][1]  # Probabilidade de ser classificado como 'Status Positivo'
                else:
                    probabilidade = probabilidade[0][0]  # Caso haja apenas uma classe
                
                if probabilidade > 0.50:
                    st.success(f"Você tem {probabilidade * 100:.2f}% de chance de ser contratado. Resultado: Sucesso")
                else:
                    st.warning(f"Você tem {probabilidade * 100:.2f}% de chance de ser contratado. Resultado: Não desista")

    st.subheader('Adicionar Nova Candidatura')
    user_id = get_user_id()
    if not user_id:
        st.warning('Por favor, insira um ID de usuário para continuar.')
        return

    df = load_data(user_id)

    with st.form(key='add_candidatura_form'):
        id_candidatura = st.text_input('ID da Candidatura')
        data_candidatura = st.date_input('Data da Candidatura')
        vaga = st.text_input('Vaga')
        nome_empresa = st.text_input('Nome da Empresa')
        link_vaga = st.text_input('Link da Vaga')
        origem_candidatura = st.text_input('Origem da Candidatura')
        pessoas_adicionadas = st.text_input('Pessoas da Empresa Adicionadas')
        linkedin_pessoa = st.text_input('Linkedin da Pessoa que Mandei a Mensagem')
        ultimo_contato = st.text_input('Último Contato pelo Linkedin')
        status = st.selectbox('Status', ['Em Processo', 'Sem Retorno', 'Com Retorno'])
        
        submit_button = st.form_submit_button(label='Adicionar Candidatura')
        if submit_button:
            if not (id_candidatura and vaga and nome_empresa and link_vaga and origem_candidatura and pessoas_adicionadas and linkedin_pessoa and ultimo_contato and status):
                st.warning('Preencha todos os dados por favor')
            else:
                new_data = pd.DataFrame({
                    'ID': [id_candidatura],
                    'Data da Candidatura': [data_candidatura],
                    'Vaga': [vaga],
                    'Nome da Empresa': [nome_empresa],
                    'Link da vaga': [link_vaga],
                    'Origem da Candidatura': [origem_candidatura],
                    'Pessoas da empresa adicionadas': [pessoas_adicionadas],
                    'Linkedin da pessoa que mandei a mensagem': [linkedin_pessoa],
                    'Último contato pelo linkedin': [ultimo_contato],
                    'Status': [status]
                })
                df = pd.concat([df, new_data], ignore_index=True)
                save_data(df, user_id)
                st.success('Candidatura adicionada com sucesso!')

    st.subheader('Excluir Candidatura')
    candidaturas = df['ID'].tolist()
    candidatura_para_deletar = st.selectbox('Selecione a candidatura para excluir', candidaturas)
    if st.button('Excluir Candidatura'):
        if candidatura_para_deletar:
            df = df[df['ID'] != candidatura_para_deletar]
            save_data(df, user_id)
            st.success('Candidatura excluída com sucesso!')

    st.subheader('Dados das Candidaturas')
    st.dataframe(df)

    st.subheader('Gráficos de Candidaturas')
    if len(df) > 0:
        if 'Data da Candidatura' in df.columns:
            df['Data da Candidatura'] = pd.to_datetime(df['Data da Candidatura'], errors='coerce')
            df = df.dropna(subset=['Data da Candidatura'])
            
            fig, ax = plt.subplots()
            df['Data da Candidatura'].value_counts().sort_index().plot(kind='bar', ax=ax)
            ax.set_xlabel('Data da Candidatura')
            ax.set_ylabel('Número de Candidaturas')
            ax.set_title('Número de Candidaturas por Data')
            st.pyplot(fig)

        st.subheader('Previsão com Modelo de Machine Learning')
        df_train = df.copy()
        model, scaler, X_columns = train_model(df_train)

        if model and scaler and X_columns:
            predict(model, scaler, X_columns)
        else:
            st.warning('Não foi possível treinar o modelo. Verifique se há dados suficientes e tente novamente.')

if __name__ == "__main__":
    run()
