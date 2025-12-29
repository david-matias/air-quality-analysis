#!/usr/bin/env python3
"""
Script principal do projeto de análise de qualidade do ar
Autor: [Seu Nome]
"""
import argparse
import sys
from src.data_collection import DataCollector

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Análise de Qualidade do Ar')
    parser.add_argument('--collect', action='store_true', help='Coletar dados')
    parser.add_argument('--dashboard', action='store_true', help='Iniciar dashboard')
    parser.add_argument('--sample', action='store_true', help='Usar dados de exemplo')
    
    args = parser.parse_args()
    
    if args.collect:
        print("🔍 Coletando dados...")
        collector = DataCollector()
        df = collector.get_data(use_sample=args.sample)
        print(f"✅ Dados coletados: {len(df)} registros")
        
    elif args.dashboard:
        print("🚀 Iniciando dashboard...")
        import subprocess
        subprocess.run(["streamlit", "run", "src/dashboard.py"])
        
    else:
        print("""
        🌍 Análise de Qualidade do Ar - Sistema
        
        Comandos disponíveis:
        python main.py --collect --sample    # Coletar dados de exemplo
        python main.py --dashboard           # Iniciar dashboard
        
        Ou execute diretamente:
        streamlit run src/dashboard.py
        jupyter notebook notebooks/
        """)

if __name__ == "__main__":
    main()