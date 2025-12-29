#!/usr/bin/env python3
"""
Script principal simplificado
"""
import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description='Sistema de Análise de Qualidade do Ar')
    
    parser.add_argument('--collect', action='store_true', help='Coletar dados')
    parser.add_argument('--clean', action='store_true', help='Limpar dados')
    parser.add_argument('--pipeline', action='store_true', help='Executar pipeline completo')
    parser.add_argument('--dashboard', action='store_true', help='Iniciar dashboard')
    parser.add_argument('--notebook', action='store_true', help='Abrir notebook')
    
    args = parser.parse_args()
    
    if args.collect:
        print("📥 Coletando dados...")
        from src.data_collection import DataCollector
        collector = DataCollector()
        df = collector.get_data(use_sample=True)
        print(f"✅ Coletados {len(df):,} registros")
    
    elif args.clean:
        print("🧹 Limpando dados...")
        from src.data_collection import DataCollector
        from src.data_cleaning import clean_air_quality_data
        collector = DataCollector()
        raw = collector.get_data(use_sample=True)
        cleaned = clean_air_quality_data(raw)
        print(f"✅ Limpos {len(cleaned):,} registros")
    
    elif args.pipeline:
        print("🚀 Executando pipeline...")
        from src.pipeline import run_full_pipeline
        run_full_pipeline()
    
    elif args.dashboard:
        print("🎨 Iniciando dashboard...")
        subprocess.run(["streamlit", "run", "src/dashboard.py"])
    
    elif args.notebook:
        print("📓 Abrindo notebook...")
        subprocess.run(["jupyter", "notebook", "notebooks/"])
    
    else:
        print("""
🌍 SISTEMA DE ANÁLISE DE QUALIDADE DO AR

Comandos:
  python main.py --collect      # Coletar dados
  python main.py --clean        # Limpar dados
  python main.py --pipeline     # Pipeline completo
  python main.py --dashboard    # Dashboard
  python main.py --notebook     # Notebook

Ou direto:
  streamlit run src/dashboard.py
  python src/pipeline.py
        """)

if __name__ == "__main__":
    main()