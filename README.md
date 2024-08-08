
# 📋 Controle de Vagas de Emprego

Bem-vindo ao projeto de **Controle de Vagas de Emprego**! Este aplicativo permite gerenciar e analisar vagas de emprego, incluindo a adição, exclusão e visualização de dados relacionados às vagas. Além disso, oferece previsões sobre a probabilidade de ser contratado com base em dados históricos.

## 🚀 Funcionalidades

- **🏠 Home**: Página inicial com animações e informações introdutórias.
- **📋 Controle de Vagas de Emprego**: Adicione, exclua e visualize vagas de emprego. Gere gráficos para análise dos dados.
- **ℹ️ Sobre o Projeto**: Informações sobre o projeto e sua finalidade.

## 💻 Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)**: Framework para criação de aplicações web interativas em Python.
- **[Pandas](https://pandas.pydata.org/)**: Biblioteca para manipulação e análise de dados.
- **[Scikit-Learn](https://scikit-learn.org/)**: Biblioteca para machine learning.
- **[Matplotlib](https://matplotlib.org/)**: Biblioteca para criação de gráficos.
- **[Streamlit Option Menu](https://github.com/tvst/st-option-menu)**: Biblioteca para menus de navegação em Streamlit.
- **[Streamlit Lottie](https://github.com/streamlit-lottie/streamlit-lottie)**: Biblioteca para animações Lottie em Streamlit.

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/thaleson/AI_Job_Vacancy_Control
   ```
2. Navegue até o diretório do projeto:
   ```bash
   cd SEU_REPOSITORIO
   ```
3. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 🛠️ Como Rodar o Projeto

1. Inicie a aplicação Streamlit:
   ```bash
   streamlit run main.py
   ```

## 📂 Estrutura do Projeto

- `main.py`: Arquivo principal para executar a aplicação Streamlit.
- `pages/`: Diretório contendo módulos para diferentes páginas.
  - `nav/home.py`: Página inicial com animações.
  - `nav/controle_vagas.py`: Página para controle e visualização de vagas.
  - `nav/sobre_projeto.py`: Página com informações sobre o projeto.
- `static/`: Diretório para arquivos estáticos.
  - `style.css`: Arquivo de estilos CSS.
- `vagas.csv`: Arquivo CSV para armazenar dados das vagas.

## 📑 Exemplo de `.gitignore`

Aqui está um exemplo de `.gitignore` para o seu projeto:

```
# Arquivos e diretórios específicos do ambiente
venv/
__pycache__/
*.pyc
*.pyo
*.pyd

# Arquivos de configuração do editor
*.vscode/
*.idea/

# Arquivos de dados temporários
*.log
*.tmp

# Arquivos do sistema operacional
.DS_Store
Thumbs.db

# Arquivo de configuração do Streamlit
*.streamlit/
```

## ✨ Contribuindo

Sinta-se à vontade para contribuir com melhorias e correções! Para isso, siga os seguintes passos:

1. Faça um fork do repositório.
2. Crie uma branch para suas alterações:
   ```bash
   git checkout -b minha-branch
   ```
3. Faça commit das suas alterações:
   ```bash
   git commit -am 'Adiciona nova funcionalidade'
   ```
4. Envie a branch para o repositório remoto:
   ```bash
   git push origin minha-branch
   ```
5. Abra um pull request para o repositório principal.

## 📜 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

-
.
