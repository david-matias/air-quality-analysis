🌍 Análise de Qualidade do Ar em Cidades Globais
Status: Em desenvolvimento 🚧
Versão: 1.0 Alpha
Data de início: 29/12/2025
Última atualização: 29/12/2025
Prazo: 12/01/2026

📋 Índice
📖 Sobre o Projeto
🎯 Objetivos
✨ Funcionalidades
🏙️ Cidades Analisadas
📊 Dataset
🛠️ Instalação e Configuração
🚀 Como Usar
📁 Estrutura do Projeto
📈 Progresso do Projeto
🔧 Tecnologias Utilizadas
📊 Resultados e Insights
🎯 Próximos Passos
📝 Licença
🙏 Agradecimentos

📖 Sobre o Projeto
Projeto de análise de dados ambientais focado na qualidade do ar em cidades globais. Desenvolvido como protótipo para demonstração de habilidades em Data Science, este projeto processa dados históricos de poluição do ar, gera visualizações interativas e inclui elementos preditivos simples.

Cliente: EcoData Analytics (startup de análise de dados ambientais)
Desenvolvedor: David Matias
Objetivo: Criar um item de portfólio reproduzível que demonstre habilidades completas em análise de dados, desde coleta até visualização e modelagem preditiva.

🎯 Objetivos
Principais:
✅ Analisar tendências de poluição atmosférica (2020-2025)
✅ Identificar padrões sazonais e geográficos
✅ Comparar níveis de poluição entre diferentes cidades globais
✅ Desenvolver dashboard interativo para visualização de dados
✅ Implementar modelo preditivo básico para poluentes

Secundários:
🔄 Criar relatório executivo com insights acionáveis
🔄 Desenvolver sistema reprodutível com dados públicos
🔄 Demonstrar boas práticas de engenharia de dados
🔄 Fornecer base para decisões ambientais e políticas públicas

✨ Funcionalidades
✅ Implementadas:
Coleta Automática de Dados: Sistema para download e processamento de dados do OpenAQ
Pipeline de Limpeza: Tratamento de valores ausentes, outliers e inconsistências
Dashboard Interativo: Visualizações com Streamlit (gráficos, mapas, filtros)
Análise Exploratória: Estatísticas descritivas, correlações, padrões temporais
Features Temporais: Criação automática de variáveis (estações, dias da semana, etc.)

🔄 Em Desenvolvimento:
Modelo preditivo de séries temporais
Mapas interativos com Folium
Sistema de alertas baseado em limites
Relatório PDF automático

🏙️ Cidades Analisadas
Cidade	País	Poluentes Monitorados
São Paulo	Brasil	PM2.5, NO2, O3
Rio de Janeiro	Brasil	PM2.5, NO2, O3
New York	EUA	PM2.5, NO2, O3
Los Angeles	EUA	PM2.5, NO2, O3
Delhi	Índia	PM2.5, NO2, O3
Mumbai	Índia	PM2.5, NO2, O3
Beijing	China	PM2.5, NO2, O3
Shanghai	China	PM2.5, NO2, O3
Tokyo	Japão	PM2.5, NO2, O3
London	Reino Unido	PM2.5, NO2, O3

📊 Dataset
Fonte Principal:
OpenAQ: Plataforma global de dados de qualidade do ar
Licença: CC-BY 4.0 (aberta para uso comercial/acadêmico)
Período: 2020-2025 (dados históricos)
Poluentes: PM2.5, NO2, O3 (principais indicadores de qualidade do ar)

Estrutura dos Dados:
python
Colunas principais:
- date: Data da medição
- city: Cidade
- parameter: Poluente (PM2.5, NO2, O3)
- value: Valor da medição (µg/m³)
- unit: Unidade de medida
- latitude/longitude: Coordenadas geográficas
- country: País
Citação Obrigatória:
text
Dados fornecidos pela OpenAQ (openaq.org) sob licença CC-BY.
Este projeto utiliza dados processados do dataset público disponível em:
https://www.kaggle.com/datasets/open-aq/openaq

🛠️ Instalação e Configuração
Pré-requisitos:
Python 3.8 ou superior
Git
4GB de RAM mínimo
2GB de espaço em disco
Passo 1: Clonar o Repositório
bash
git clone https://github.com/seu-usuario/air-quality-analysis.git
cd air-quality-analysis
Passo 2: Criar Ambiente Virtual (Recomendado)
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Passo 3: Instalar Dependências
bash
pip install -r requirements.txt
Passo 4: Verificar Instalação
bash
python -c "import pandas; import streamlit; print('✅ Instalação bem-sucedida!')"
🚀 Como Usar
Opção 1: Pipeline Completo (Recomendado para Primeira Execução)
bash
python src/pipeline.py

Este comando executa todas as etapas:
Coleta de dados
Limpeza e processamento
Análise básica
Geração de datasets finais

Opção 2: Dashboard Interativo
bash
streamlit run src/dashboard.py
Acesse no navegador: http://localhost:8501

Opção 3: Script Principal com Opções
bash
# Coletar dados
python main.py --collect

# Limpar dados
python main.py --clean

# Pipeline completo
python main.py --pipeline

# Dashboard
python main.py --dashboard

# Notebook Jupyter
python main.py --notebook
Opção 4: Uso Direto dos Módulos
python
# Exemplo de uso em Python
from src.data_collection import DataCollector
from src.data_cleaning import clean_air_quality_data

# Coletar dados
collector = DataCollector()
raw_data = collector.get_data(use_sample=True)

# Limpar dados
clean_data = clean_air_quality_data(raw_data, save_path='data/processed/')
📁 Estrutura do Projeto
text
air-quality-analysis/
├── 📂 src/                    # Código fonte
│   ├── __init__.py           # Inicialização do módulo
│   ├── data_collection.py    # Coleta de dados do OpenAQ
│   ├── data_cleaning.py      # Limpeza e processamento
│   ├── pipeline.py           # Pipeline completo
│   └── dashboard.py          # Dashboard Streamlit
│
├── 📂 notebooks/             # Análise exploratória
│   └── 01_exploratory_analysis.ipynb
│
├── 📂 data/                  # Dados
│   ├── raw/                  # Dados brutos
│   └── processed/            # Dados processados
│
├── 📂 docs/                  # Documentação
├── 📂 tests/                 # Testes unitários
├── 📂 reports/               # Relatórios gerados
│
├── 📄 main.py                # Script principal
├── 📄 requirements.txt       # Dependências Python
├── 📄 README.md              # Esta documentação
├── 📄 LICENSE               # Licença MIT
└── 📄 .gitignore            # Arquivos ignorados pelo Git
📈 Progresso do Projeto
✅ Concluído (Fase 1 - Alpha):
Estrutura do Projeto: Organização modular e profissional
Coleta de Dados: Sistema robusto com fallback para dados de exemplo
Pipeline de Limpeza: Tratamento completo de dados (missing values, outliers, etc.)
Dashboard Básico: Interface Streamlit com visualizações interativas
Análise Exploratória: Notebook Jupyter com primeiras análises
Documentação: README completo e instruções de uso

🔄 Em Andamento (Fase 2 - Beta):
Modelo Preditivo: Implementação de ARIMA/Prophet para previsões
Visualizações Avançadas: Mapas interativos, heatmaps, gráficos 3D
Sistema de Alertas: Notificações baseadas em limites de qualidade do ar
Otimização: Melhoria de performance para grandes volumes de dados

📅 Planejado (Fase 3 - Release):
API REST: Endpoints para consulta de dados
Relatório Automático: Geração de PDF com insights
Deploy Cloud: Hospedagem do dashboard online
Integração Contínua: CI/CD com GitHub Actions

🔧 Tecnologias Utilizadas
Linguagens e Frameworks:
Python 3.8+: Linguagem principal
Pandas: Manipulação de dados
NumPy: Cálculos numéricos
Scikit-learn: Machine Learning
Streamlit: Dashboard web
Jupyter: Análise exploratória

Visualização:
Matplotlib/Seaborn: Gráficos estáticos
Plotly: Gráficos interativos
Folium: Mapas geográficos (em implementação)

Ferramentas:
Git/GitHub: Versionamento e colaboração
VS Code: Ambiente de desenvolvimento
Docker: Containerização (opcional)

Boas Práticas Implementadas:
✅ Código modular e reutilizável
✅ Tratamento robusto de erros
✅ Documentação clara
✅ Versionamento semântico
✅ Ambiente virtual isolado

📊 Resultados e Insights
Insights Iniciais (Baseados em Dados de Exemplo):
Cidades Mais Poluídas (Média PM2.5):
Delhi e Beijing apresentam os maiores níveis
Cidades europeias e japonesas têm os menores índices
Padrões Sazonais:
Maiores concentrações no inverno (combustão para aquecimento)
Menores concentrações no verão (dispersão atmosférica)

Correlações:
Forte correlação entre poluentes em uma mesma cidade
Relação inversa entre temperatura e alguns poluentes
Tendências Temporais:
Redução gradual em algumas cidades (2020-2023)
Picos associados a eventos específicos

Visualizações Disponíveis no Dashboard:
📈 Gráfico de linhas: Tendência temporal por cidade
📊 Boxplots: Distribuição por poluente
🏙️ Comparativo entre cidades
📋 Tabela interativa com dados filtrados

🎯 Próximos Passos
Curto Prazo (Esta Semana):
Implementar modelo preditivo com scikit-learn
Adicionar mapas interativos com Folium
Criar sistema de filtros avançados no dashboard
Otimizar performance do pipeline
Médio Prazo (Próximas 2 Semanas):
Desenvolver API REST com FastAPI
Implementar cache para melhor performance
Criar relatório PDF automático
Adicionar testes unitários
Longo Prazo (Extensões Futuras):
Deploy em cloud (AWS/Azure/Google Cloud)
Integração com APIs em tempo real
Sistema de alertas por email/telegram
Análise de impacto econômico da poluição

📝 Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.
text
MIT License
Copyright (c) 2025 David Matias
Permissão é concedida, gratuitamente, a qualquer pessoa que obtenha uma cópia
deste software e dos arquivos de documentação associados (o "Software"), para lidar
no Software sem restrição, incluindo, sem limitação, os direitos de usar, copiar,
modificar, mesclar, publicar, distribuir, sublicenciar e/ou vender cópias do Software,
e para permitir que as pessoas a quem o Software é fornecido o façam, sujeito às
seguintes condições:

O aviso de copyright acima e este aviso de permissão devem ser incluídos em todas
as cópias ou partes substanciais do Software.
🙏 Agradecimentos
OpenAQ: Pelo dataset público e de qualidade
Comunidade Python: Pelas bibliotecas open-source
Kaggle: Pela hospedagem dos datasets
Streamlit: Pelo framework incrível para dashboards

🔗 Links Úteis
Repositório GitHub
Dataset OpenAQ no Kaggle
Documentação OpenAQ
Documentação Streamlit

📧 Contato
Desenvolvedor: David Matias
Email: [davidmatias8@gmail.com]

Nota: Este é um projeto em desenvolvimento. Novas funcionalidades são adicionadas regularmente. Consulte o CHANGELOG.md para acompanhar as atualizações.

*Última atualização: 29/12/2025*