"""
Dashboard Streamlit para análise de qualidade do ar
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Qualidade do Ar",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

class AirQualityDashboard:
    def __init__(self):
        self.df = None
        self.load_data()
    
    def load_data(self):
        """Carrega os dados processados"""
        try:
            from data_collection import DataCollector
            collector = DataCollector()
            self.df = collector.get_data(use_sample=True)
        except:
            st.error("Erro ao carregar dados. Usando dados de exemplo...")
            # Dados de exemplo como fallback
            self.df = pd.DataFrame({
                'date': pd.date_range('2020-01-01', '2023-12-31', freq='D'),
                'city': ['São Paulo'] * 1461,
                'parameter': ['PM2.5'] * 1461,
                'value': np.random.normal(30, 10, 1461)
            })
    
    def create_sidebar(self):
        """Cria a barra lateral com filtros"""
        st.sidebar.title("🔍 Filtros")
        
        # Filtro de cidades
        cities = st.sidebar.multiselect(
            "Selecione as cidades:",
            options=sorted(self.df['city'].unique()),
            default=['São Paulo', 'Delhi', 'New York']
        )
        
        # Filtro de poluentes
        pollutants = st.sidebar.multiselect(
            "Selecione os poluentes:",
            options=sorted(self.df['parameter'].unique()),
            default=['PM2.5', 'NO2']
        )
        
        # Filtro de data
        min_date = pd.to_datetime(self.df['date']).min()
        max_date = pd.to_datetime(self.df['date']).max()
        
        date_range = st.sidebar.date_input(
            "Selecione o período:",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        return cities, pollutants, date_range
    
    def create_main_content(self, cities, pollutants, date_range):
        """Cria o conteúdo principal do dashboard"""
        
        # Filtrar dados
        filtered_df = self.df[
            (self.df['city'].isin(cities)) &
            (self.df['parameter'].isin(pollutants))
        ]
        
        if len(date_range) == 2:
            filtered_df = filtered_df[
                (pd.to_datetime(filtered_df['date']) >= pd.to_datetime(date_range[0])) &
                (pd.to_datetime(filtered_df['date']) <= pd.to_datetime(date_range[1]))
            ]
        
        # Título
        st.title("🌍 Dashboard de Qualidade do Ar")
        st.markdown("---")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_pm25 = filtered_df[filtered_df['parameter'] == 'PM2.5']['value'].mean()
            st.metric("Média PM2.5", f"{avg_pm25:.1f} µg/m³")
        
        with col2:
            max_pollutant = filtered_df.groupby('parameter')['value'].mean().idxmax()
            st.metric("Poluente Mais Alto", max_pollutant)
        
        with col3:
            worst_city = filtered_df.groupby('city')['value'].mean().idxmax()
            st.metric("Cidade Mais Poluída", worst_city)
        
        with col4:
            total_records = len(filtered_df)
            st.metric("Total de Registros", f"{total_records:,}")
        
        st.markdown("---")
        
        # Gráfico 1: Tendências temporais
        st.subheader("📈 Tendências Temporais")
        
        fig1 = px.line(
            filtered_df,
            x='date',
            y='value',
            color='city',
            line_dash='parameter',
            title='Evolução da Qualidade do Ar',
            labels={'value': 'Concentração (µg/m³)', 'date': 'Data'}
        )
        st.plotly_chart(fig1, use_container_width=True)
        
        # Gráfico 2: Comparação entre cidades
        st.subheader("🏙️ Comparação entre Cidades")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig2 = px.box(
                filtered_df,
                x='city',
                y='value',
                color='parameter',
                title='Distribuição por Cidade'
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with col2:
            city_avg = filtered_df.groupby(['city', 'parameter'])['value'].mean().reset_index()
            fig3 = px.bar(
                city_avg,
                x='city',
                y='value',
                color='parameter',
                barmode='group',
                title='Média por Cidade e Poluente'
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        # Mapa
        st.subheader("🗺️ Mapa de Poluição")
        
        # Criar mapa
        m = folium.Map(location=[20, 0], zoom_start=2)
        
        # Adicionar marcadores (simplificado)
        for city in cities:
            city_data = filtered_df[filtered_df['city'] == city]
            if not city_data.empty:
                avg_value = city_data['value'].mean()
                
                # Definir cor baseada no nível de poluição
                color = 'green' if avg_value < 20 else 'orange' if avg_value < 50 else 'red'
                
                folium.Marker(
                    location=[city_data['latitude'].iloc[0], city_data['longitude'].iloc[0]],
                    popup=f"{city}<br>Média: {avg_value:.1f} µg/m³",
                    icon=folium.Icon(color=color, icon='info-sign')
                ).add_to(m)
        
        folium_static(m, width=1000, height=500)
        
        # Tabela de dados
        st.subheader("📋 Dados Filtrados")
        st.dataframe(filtered_df.head(100), use_container_width=True)
        
        # Download dos dados filtrados
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download dos dados filtrados",
            data=csv,
            file_name="air_quality_filtered.csv",
            mime="text/csv"
        )

def main():
    """Função principal do dashboard"""
    st.sidebar.image("https://img.icons8.com/color/96/000000/air-element.png", width=100)
    
    dashboard = AirQualityDashboard()
    
    # Carregar filtros da sidebar
    cities, pollutants, date_range = dashboard.create_sidebar()
    
    # Mostrar conteúdo principal
    dashboard.create_main_content(cities, pollutants, date_range)
    
    # Informações do projeto
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ Sobre o Projeto")
    st.sidebar.info("""
    **Dashboard de Análise de Qualidade do Ar**
    
    - **Fonte:** OpenAQ
    - **Período:** 2020-2025
    - **Poluentes:** PM2.5, NO2, O3
    - **Cidades:** 10 globais
    
    [GitHub do Projeto](https://github.com/seu-usuario/air-quality-analysis)
    """)

if __name__ == "__main__":
    main()