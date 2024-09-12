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
            df = pd.DataFrame(columns=['Nome_da_Empresa', 'Localizacao', 'Link_da_Vaga', 'Progresso', 
                                       'Data_da_Aplicacao', 'Tipo_de_Vaga', 'Setor', 'Data_da_Candidatura', 
                                       'Vaga', 'Origem_da_Candidatura', 'Pessoas_da_Empresa_Adicionadas', 
                                       'Linkedin_da_Pessoa_que_Mandei_a_Mensagem', 'Ultimo_Contato_pelo_Linkedin', 
                                       'Status'])
            df.to_csv(file_path, index=False)
        return pd.read_csv(file_path)

    def save_data(df, user_id):
        df.to_csv(f'{user_id}_vagas.csv', index=False)

    def prepare_features(data):
        le_status = LabelEncoder()
        data['Status_encoded'] = le_status.fit_transform(data['Status'])

        try:
            data['Data_da_Candidatura'] = pd.to_datetime(data['Data_da_Candidatura'], format='%Y-%m-%d', errors='coerce')
            data = data.dropna(subset=['Data_da_Candidatura'])
            data['Data_da_Candidatura'] = data['Data_da_Candidatura'].map(datetime.toordinal)
        except Exception as e:
            st.error(f"Erro ao converter datas: {e}")
            return None, None, None, None

        X = data[['Data_da_Candidatura', 'Vaga', 'Origem_da_Candidatura', 'Pessoas_da_Empresa_Adicionadas', 
                  'Linkedin_da_Pessoa_que_Mandei_a_Mensagem', 'Ultimo_Contato_pelo_Linkedin']]
        y = data['Status_encoded']

        # Verificar se há dados suficientes e remover valores nulos
        if X.isnull().sum().sum() > 0 or y.isnull().sum() > 0:
            st.error('Existem valores nulos nos dados.')
            return None, None, None, None

        X = pd.get_dummies(X, drop_first=True)
        X_columns = X.columns
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        return X, y, scaler, X_columns

    def train_model(data):
        X, y, scaler, X_columns = prepare_features(data)

        if X is None or y is None:
            return None, None, None

        # Verificar se há dados suficientes
        if len(X) < 2 or len(set(y)) < 2:
            st.error('Dados insuficientes para treinar o modelo.')
            return None, None, None

        # Verificar se X e y são arrays válidos
        if X.shape[0] == 0 or len(y) == 0:
            st.error('Dados de entrada inválidos.')
            return None, None, None

        # Dividir dados
        try:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        except ValueError as e:
            st.error(f'Erro ao dividir os dados: {e}')
            return None, None, None

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        scores = cross_val_score(model, X, y, cv=5)
        st.write(f"Acurácia média do modelo: {scores.mean():.2f}")

        return model, scaler, X_columns

    def predict(model, scaler, X_columns):
        data_hoje = st.date_input('Data da Candidatura para Previsão', datetime.today())
        vaga_previsao = st.text_input('Vaga para Previsão')
        origem_previsao = st.text_input('Origem da Candidatura')
        pessoas_adicionadas_previsao = st.text_input('Pessoas da Empresa Adicionadas')
        linkedin_previsao = st.text_input('Linkedin da Pessoa que Mandei a Mensagem')
        ultimo_contato_previsao = st.text_input('Último Contato pelo Linkedin')

        if st.button('Prever'):
            if not (vaga_previsao and origem_previsao and pessoas_adicionadas_previsao and linkedin_previsao and ultimo_contato_previsao):
                st.warning('Preencha todos os dados para análise e previsão do modelo')
            else:
                data_hoje_ordinal = datetime.toordinal(data_hoje)
                input_features = pd.DataFrame([[data_hoje_ordinal, vaga_previsao, origem_previsao, pessoas_adicionadas_previsao, linkedin_previsao, ultimo_contato_previsao]],
                                            columns=['Data_da_Candidatura', 'Vaga', 'Origem_da_Candidatura', 'Pessoas_da_Empresa_Adicionadas', 
                                                     'Linkedin_da_Pessoa_que_Mandei_a_Mensagem', 'Ultimo_Contato_pelo_Linkedin'])
                
                input_features = pd.get_dummies(input_features, drop_first=True)
                input_features = input_features.reindex(columns=X_columns, fill_value=0)
                input_features = scaler.transform(input_features)
                
                probabilidade = model.predict_proba(input_features)
                
                if probabilidade.shape[1] > 1:
                    probabilidade = probabilidade[0][1]  # Probabilidade de ser classificado como 'Com Retorno'
                else:
                    probabilidade = probabilidade[0][0]  # Caso haja apenas uma classe
                
                if probabilidade > 0.50:
                    st.success(f"Você tem {probabilidade * 100:.2f}% de chance de ser contratado. Resultado: Sucesso")
                else:
                    st.warning(f"Você tem {probabilidade * 100:.2f}% de chance de ser contratado. Resultado: Não desista")

    st.subheader('Adicionar Nova Vaga')
    user_id = get_user_id()
    if not user_id:
        st.warning('Por favor, insira um ID de usuário para continuar.')
        return

    df = load_data(user_id)

    with st.form(key='add_vaga_form'):
        nome_empresa = st.text_input('Nome da Empresa')
        localizacao = st.text_input('Localização')
        link_vaga = st.text_input('Link da Vaga')
        progresso = st.selectbox('Progresso', ['Em Processo', 'Sem Retorno', 'Com Retorno'])
        data_aplicacao = st.date_input('Data da Aplicação')
        tipo_vaga = st.selectbox('Tipo de Vaga', ['Full-time', 'Part-time', 'Freelance', 'Internship'])
        setor = st.text_input('Setor')
        data_candidatura = st.date_input('Data da Candidatura')
        vaga = st.text_input('Vaga')
        origem_candidatura = st.text_input('Origem da Candidatura')
        pessoas_adicionadas = st.text_input('Pessoas da Empresa Adicionadas')
        linkedin_mensagem = st.text_input('Linkedin da Pessoa que Mandei a Mensagem')
        ultimo_contato = st.text_input('Último Contato pelo Linkedin')
        status = st.selectbox('Status', ['Em Processo', 'Sem Retorno', 'Com Retorno'])
        
        submit_button = st.form_submit_button(label='Adicionar Vaga')
        if submit_button:
            if not (nome_empresa and localizacao and link_vaga and progresso and data_aplicacao and tipo_vaga and setor and data_candidatura and vaga and origem_candidatura and pessoas_adicionadas and linkedin_mensagem and ultimo_contato and status):
                st.warning('Preencha todos os dados por favor')
            else:
                new_data = pd.DataFrame({
                    'Nome_da_Empresa': [nome_empresa],
                    'Localizacao': [localizacao],
                    'Link_da_Vaga': [link_vaga],
                    'Progresso': [progresso],
                    'Data_da_Aplicacao': [data_aplicacao],
                    'Tipo_de_Vaga': [tipo_vaga],
                    'Setor': [setor],
                    'Data_da_Candidatura': [data_candidatura],
                    'Vaga': [vaga],
                    'Origem_da_Candidatura': [origem_candidatura],
                    'Pessoas_da_Empresa_Adicionadas': [pessoas_adicionadas],
                    'Linkedin_da_Pessoa_que_Mandei_a_Mensagem': [linkedin_mensagem],
                    'Ultimo_Contato_pelo_Linkedin': [ultimo_contato],
                    'Status': [status]
                })
                df = pd.concat([df, new_data], ignore_index=True)
                save_data(df, user_id)
                st.success('Vaga adicionada com sucesso!')

    if st.button('Treinar Modelo'):
        if len(df) < 2:
            st.error('Não há dados suficientes para treinar o modelo.')
        else:
            model, scaler, X_columns = train_model(df)
            if model is not None:
                st.success('Modelo treinado com sucesso!')
                predict(model, scaler, X_columns)
            else:
                st.error('Erro ao treinar o modelo.')

if __name__ == "__main__":
    run()
