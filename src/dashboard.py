"""
Dashboard Streamlit simplificado
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração
st.set_page_config(
    page_title="Dashboard de Qualidade do Ar",
    page_icon="🌍",
    layout="wide"
)

@st.cache_data
def load_data():
    """Carrega os dados processados"""
    try:
        return pd.read_parquet('data/processed/final_dataset.parquet')
    except:
        # Fallback para dados de exemplo
        from data_collection import DataCollector
        from data_cleaning import clean_air_quality_data
        collector = DataCollector()
        raw = collector.get_data(use_sample=True)
        return clean_air_quality_data(raw, save_path=None)

def main():
    st.title("🌍 Dashboard de Qualidade do Ar")
    st.markdown("Análise de poluição em cidades globais (2020-2023)")
    
    # Carregar dados
    df = load_data()
    
    # Sidebar
    st.sidebar.title("🔍 Filtros")
    
    cities = st.sidebar.multiselect(
        "Cidades:",
        options=sorted(df['city'].unique()),
        default=['São Paulo', 'Delhi', 'New York']
    )
    
    pollutants = st.sidebar.multiselect(
        "Poluentes:",
        options=sorted(df['parameter'].unique()),
        default=['PM2.5']
    )
    
    # Filtrar
    filtered_df = df[
        (df['city'].isin(cities)) &
        (df['parameter'].isin(pollutants))
    ]
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        avg = filtered_df['value'].mean()
        st.metric("Média Geral", f"{avg:.1f} µg/m³")
    with col2:
        worst_city = filtered_df.groupby('city')['value'].mean().idxmax()
        st.metric("Cidade Mais Poluída", worst_city)
    with col3:
        total = len(filtered_df)
        st.metric("Total de Registros", f"{total:,}")
    
    st.markdown("---")
    
    # Gráfico 1: Tendência temporal
    st.subheader("📈 Tendência Temporal")
    
    if not filtered_df.empty:
        fig1 = px.line(
            filtered_df,
            x='date',
            y='value',
            color='city',
            line_dash='parameter',
            title='Evolução da Poluição'
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
            title='Média por Cidade'
        )
        st.plotly_chart(fig3, use_container_width=True)
    
    # Tabela
    st.subheader("📋 Dados Filtrados")
    st.dataframe(filtered_df.head(50), use_container_width=True)
    
    # Download
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="air_quality_data.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()