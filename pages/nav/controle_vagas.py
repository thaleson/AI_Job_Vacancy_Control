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

    # Função para carregar o CSV
    def load_data():
        if not os.path.exists('vagas.csv'):
            df = pd.DataFrame(columns=['Nome_da_Empresa', 'Localizacao', 'Link_da_Vaga', 'Progresso', 'Data_da_Aplicacao', 'Tipo_de_Vaga', 'Setor'])
            df.to_csv('vagas.csv', index=False)
        return pd.read_csv('vagas.csv')

    # Função para salvar o CSV
    def save_data(df):
        df.to_csv('vagas.csv', index=False)
    
    # Função para resetar o CSV
    def reset_csv():
        """Função para resetar o arquivo CSV, deixando-o vazio."""
        df = pd.DataFrame(columns=['Nome_da_Empresa', 'Localizacao', 'Link_da_Vaga', 'Progresso', 'Data_da_Aplicacao', 'Tipo_de_Vaga', 'Setor'])
        df.to_csv('vagas.csv', index=False)
        st.success('CSV foi resetado e está vazio!')

    # Função para preparar os dados
    def prepare_features(data):
        # Codificar variáveis categóricas
        le_progresso = LabelEncoder()
        data['Progresso_encoded'] = le_progresso.fit_transform(data['Progresso'])

        # Converter datas
        try:
            data['Data_da_Aplicacao'] = pd.to_datetime(data['Data_da_Aplicacao'], format='%Y-%m-%d', errors='coerce')
            data = data.dropna(subset=['Data_da_Aplicacao'])  # Remove linhas com datas inválidas
            data['Data_da_Aplicacao'] = data['Data_da_Aplicacao'].map(datetime.toordinal)
        except Exception as e:
            st.error(f"Erro ao converter datas: {e}")
            return None, None, None, None

        X = data[['Data_da_Aplicacao', 'Tipo_de_Vaga', 'Setor']]
        y = data['Progresso_encoded']
        
        # Codificar variáveis categóricas adicionais
        X = pd.get_dummies(X, columns=['Tipo_de_Vaga', 'Setor'], drop_first=True)
        
        # Obter nomes das colunas antes da normalização
        X_columns = X.columns
        
        # Normalizar dados
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        return X, y, scaler, X_columns

    def train_model(data):
        X, y, scaler, X_columns = prepare_features(data)
        
        if X is None or y is None:  # Verifica se os dados foram preparados corretamente
            return None, None, None
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        # Avaliar o modelo
        scores = cross_val_score(model, X, y, cv=5)
        st.write(f"Acurácia média do modelo: {scores.mean():.2f}")
        
        return model, scaler, X_columns

    def predict(model, scaler, X_columns):
        # Dados para previsão
        data_hoje = st.date_input('Data da Aplicação para Previsão', datetime.today())
        tipo_vaga_previsao = st.selectbox('Tipo de Vaga para Previsão', ['Full-time', 'Part-time', 'Freelance', 'Internship'])
        setor_previsao = st.text_input('Setor para Previsão')

        if st.button('Prever'):
            if not (tipo_vaga_previsao and setor_previsao):
                st.warning('Preencha todos os dados para análise e previsão do modelo')
            else:
                # Preparar dados para a previsão
                data_hoje_ordinal = datetime.toordinal(data_hoje)
                input_features = pd.DataFrame([[data_hoje_ordinal, tipo_vaga_previsao, setor_previsao]],
                                            columns=['Data_da_Aplicacao', 'Tipo_de_Vaga', 'Setor'])
                
                # Codificar variáveis categóricas e normalizar
                input_features = pd.get_dummies(input_features, columns=['Tipo_de_Vaga', 'Setor'], drop_first=True)
                input_features = input_features.reindex(columns=X_columns, fill_value=0)
                input_features = scaler.transform(input_features)
                
                probabilidade = model.predict_proba(input_features)
                
                  
                if probabilidade.shape[1] > 1:
                    probabilidade = probabilidade[0][1]  # Probabilidade de ser classificado como 'Com Retorno'
                else:
                    probabilidade = probabilidade[0][0]  # Caso haja apenas uma classe
                
                if probabilidade > 0.50:
                    st.success(f"Você tem {probabilidade:.2f} de chance de ser contratado. Resultado: Sucesso")
                else:
                    st.warning(f"Você tem {probabilidade:.2f} de chance de ser contratado. Resultado: Não desista")

    # Adicionar nova vaga
    st.subheader('Adicionar Nova Vaga')
    with st.form(key='add_vaga_form'):
        nome_empresa = st.text_input('Nome da Empresa')
        localizacao = st.text_input('Localização')
        link_vaga = st.text_input('Link da Vaga')
        progresso = st.selectbox('Progresso', ['Em Processo', 'Sem Retorno', 'Com Retorno'])
        data_aplicacao = st.date_input('Data da Aplicação')
        tipo_vaga = st.selectbox('Tipo de Vaga', ['Full-time', 'Part-time', 'Freelance', 'Internship'])
        setor = st.text_input('Setor')
        
        submit_button = st.form_submit_button(label='Adicionar Vaga')
        if submit_button:
            if not (nome_empresa and localizacao and link_vaga and progresso and data_aplicacao and tipo_vaga and setor):
                st.warning('Preencha todos os dados por favor')
            else:
                new_data = pd.DataFrame({
                    'Nome_da_Empresa': [nome_empresa],
                    'Localizacao': [localizacao],
                    'Link_da_Vaga': [link_vaga],
                    'Progresso': [progresso],
                    'Data_da_Aplicacao': [data_aplicacao],
                    'Tipo_de_Vaga': [tipo_vaga],
                    'Setor': [setor]
                })
                df = load_data()
                df = pd.concat([df, new_data], ignore_index=True)
                save_data(df)
                st.success('Vaga adicionada com sucesso!')

    # Excluir vaga
    st.subheader('Excluir Vaga')
    df = load_data()
    vagas = df['Nome_da_Empresa'].tolist()
    vaga_para_deletar = st.selectbox('Selecione a vaga para excluir', vagas)
    if st.button('Excluir Vaga'):
        if vaga_para_deletar:
            df = df[df['Nome_da_Empresa'] != vaga_para_deletar]
            save_data(df)
            st.success('Vaga excluída com sucesso!')

    # Mostrar dados do CSV
    st.subheader('Dados das Vagas')
    df = load_data()
    st.dataframe(df)

    # Gráficos
    st.subheader('Gráficos de Vagas')
    if len(df) > 0:
        df['Data_da_Aplicacao'] = pd.to_datetime(df['Data_da_Aplicacao'], errors='coerce')
        df = df.dropna(subset=['Data_da_Aplicacao'])  # Remove linhas com datas inválidas
        
        # Gráfico de linha das vagas por data
        fig, ax = plt.subplots()
        df['Quantidade'] = 1
        df_grouped = df.groupby('Data_da_Aplicacao').count()
        df_grouped['Quantidade'].plot(ax=ax)
        ax.set_title('Número de Vagas ao Longo do Tempo')
        ax.set_xlabel('Data da Aplicação')
        ax.set_ylabel('Quantidade de Vagas')
        st.pyplot(fig)
        
        # Gráfico de barras do progresso das vagas
        fig, ax = plt.subplots()
        progresso_counts = df['Progresso'].value_counts()
        progresso_counts.plot(kind='bar', ax=ax)
        ax.set_title('Distribuição de Progresso das Vagas')
        ax.set_xlabel('Progresso')
        ax.set_ylabel('Quantidade de Vagas')
        st.pyplot(fig)
        
        # Gráfico de pizza dos tipos de vaga
        fig, ax = plt.subplots()
        tipo_vaga_counts = df['Tipo_de_Vaga'].value_counts()
        ax.pie(tipo_vaga_counts, labels=tipo_vaga_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribuição dos Tipos de Vaga')
        st.pyplot(fig)
        
        # Gráfico de pizza dos setores
        fig, ax = plt.subplots()
        setor_counts = df['Setor'].value_counts()
        ax.pie(setor_counts, labels=setor_counts.index, autopct='%1.1f%%', startangle=90)
        ax.set_title('Distribuição dos Setores')
        st.pyplot(fig)

    if len(df) > 10:  # Treinar o modelo se tivermos dados suficientes
        model, scaler, X_columns = train_model(df)
        
        st.subheader('Previsão de Contratação')
        if model is not None and scaler is not None and X_columns is not None:  # Verifica se o modelo foi treinado corretamente
            predict(model, scaler, X_columns)

    # Seção para resetar o CSV
    st.subheader('Resetar CSV')
    if st.button('Resetar CSV'):
        reset_csv()

# Para rodar o app
if __name__ == '__main__':
    run()
