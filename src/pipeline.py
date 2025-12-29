"""
Pipeline completo do projeto
"""
import pandas as pd
import numpy as np
from datetime import datetime
import sys
import os

def run_full_pipeline():
    """Executa o pipeline completo"""
    
    print("🚀 INICIANDO PIPELINE COMPLETO")
    print("=" * 60)
    
    # 1. Coleta
    print("\n📥 FASE 1: COLETA DE DADOS")
    from data_collection import DataCollector
    collector = DataCollector()
    raw_data = collector.get_data(use_sample=True)
    print(f"✅ Dados brutos: {len(raw_data):,} registros")
    
    # 2. Limpeza
    print("\n🧹 FASE 2: LIMPEZA DE DADOS")
    from data_cleaning import clean_air_quality_data
    cleaned_data = clean_air_quality_data(raw_data, save_path='data/processed/')
    print(f"✅ Dados limpos: {len(cleaned_data):,} registros")
    
    # 3. Análise básica
    print("\n📊 FASE 3: ANÁLISE BÁSICA")
    
    # Estatísticas
    stats = cleaned_data.groupby(['city', 'parameter'])['value'].agg([
        'count', 'mean', 'std', 'min', 'max'
    ]).round(2)
    
    print("Estatísticas por cidade e poluente:")
    print(stats.head(10))
    
    # 4. Salvar resultados
    print("\n💾 FASE 4: SALVANDO RESULTADOS")
    
    # Salvar em Parquet (mais eficiente)
    final_path = 'data/processed/final_dataset.parquet'
    cleaned_data.to_parquet(final_path, index=False)
    print(f"✅ Dataset final: {final_path}")
    
    # Sumário
    summary_path = 'data/processed/summary.txt'
    with open(summary_path, 'w') as f:
        f.write(f"RESUMO DO PROJETO\n")
        f.write(f"Gerado: {datetime.now()}\n")
        f.write(f"Total registros: {len(cleaned_data):,}\n")
        f.write(f"Cidades: {cleaned_data['city'].nunique()}\n")
        f.write(f"Poluentes: {', '.join(cleaned_data['parameter'].unique())}\n")
        f.write(f"Período: {cleaned_data['date'].min()} a {cleaned_data['date'].max()}\n")
    
    print(f"✅ Sumário: {summary_path}")
    
    print("\n" + "=" * 60)
    print("🎉 PIPELINE CONCLUÍDO!")
    print("=" * 60)
    
    print("\n📋 PRÓXIMOS PASSOS:")
    print("1. Dashboard: streamlit run src/dashboard.py")
    print("2. Notebook: jupyter notebook notebooks/")
    
    return cleaned_data

if __name__ == "__main__":
    run_full_pipeline()