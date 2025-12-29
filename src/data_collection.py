"""
Módulo para coleta de dados da OpenAQ
Autor: [David Matias]
Data: 29/12/2025
"""
import pandas as pd
import numpy as np
import os
from datetime import datetime
import requests
import zipfile
import io
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')

class DataCollector:
    """Classe para coleta de dados de qualidade do ar"""
    
    def __init__(self, data_dir='./data'):
        """
        Inicializa o coletor de dados
        
        Args:
            data_dir (str): Diretório para salvar os dados
        """
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, 'raw')
        self.processed_dir = os.path.join(data_dir, 'processed')
        
        # Criar diretórios se não existirem
        os.makedirs(self.raw_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
        
        # Cidades selecionadas (pode ajustar)
        self.cities = [
            'São Paulo', 'Rio de Janeiro',
            'New York', 'Los Angeles',
            'Delhi', 'Mumbai',
            'Beijing', 'Shanghai',
            'Tokyo', 'London'
        ]
        
        # Poluentes principais
        self.pollutants = ['PM2.5', 'NO2', 'O3']
        
        # Período de interesse
        self.start_date = '2020-01-01'
        self.end_date = '2025-12-31'
    
    def download_from_kaggle(self):
        """
        Download do dataset do Kaggle
        Nota: Requer configuração da API do Kaggle
        """
        print("📥 Método 1: Download do Kaggle")
        try:
            # Para usar este método, configure a API do Kaggle:
            # 1. Crie token em https://www.kaggle.com/settings
            # 2. Salve kaggle.json em ~/.kaggle/
            
            from kaggle.api.kaggle_api_extended import KaggleApi
            api = KaggleApi()
            api.authenticate()
            
            api.dataset_download_files(
                'open-aq/openaq',
                path=self.raw_dir,
                unzip=True
            )
            print("✅ Download do Kaggle concluído!")
            return True
            
        except Exception as e:
            print(f"❌ Erro no download do Kaggle: {e}")
            print("🔄 Tentando método alternativo...")
            return False
    
    def download_sample_data(self):
        """
        Método alternativo: Usar dados de amostra ou baixar via API
        """
        print("📥 Método 2: Criando dataset de exemplo para desenvolvimento")
        
        # Criar dados sintéticos para desenvolvimento inicial
        np.random.seed(42)
        dates = pd.date_range(self.start_date, self.end_date, freq='D')
        num_days = len(dates)
        
        data = []
        for city in self.cities:
            for pollutant in self.pollutants:
                # Valores base por cidade e poluente
                if 'Delhi' in city or 'Beijing' in city:
                    base_value = np.random.uniform(50, 200)
                elif 'São Paulo' in city or 'Mumbai' in city:
                    base_value = np.random.uniform(30, 100)
                else:
                    base_value = np.random.uniform(10, 50)
                
                # Adicionar sazonalidade
                for i, date in enumerate(dates):
                    # Variação sazonal
                    seasonal = 20 * np.sin(2 * np.pi * i / 365)
                    
                    # Variação aleatória
                    random_var = np.random.normal(0, 10)
                    
                    value = max(0, base_value + seasonal + random_var)
                    
                    data.append({
                        'date': date,
                        'city': city,
                        'country': self._get_country(city),
                        'parameter': pollutant,
                        'value': round(value, 2),
                        'unit': 'µg/m³',
                        'latitude': self._get_coordinates(city)[0],
                        'longitude': self._get_coordinates(city)[1]
                    })
        
        df = pd.DataFrame(data)
        
        # Salvar dados
        sample_path = os.path.join(self.raw_dir, 'sample_data.csv')
        df.to_csv(sample_path, index=False)
        
        print(f"✅ Dataset de exemplo criado: {len(df)} registros")
        print(f"💾 Salvo em: {sample_path}")
        
        return df
    
    def _get_country(self, city):
        """Retorna país baseado na cidade"""
        countries = {
            'São Paulo': 'Brazil',
            'Rio de Janeiro': 'Brazil',
            'New York': 'USA',
            'Los Angeles': 'USA',
            'Delhi': 'India',
            'Mumbai': 'India',
            'Beijing': 'China',
            'Shanghai': 'China',
            'Tokyo': 'Japan',
            'London': 'United Kingdom'
        }
        return countries.get(city, 'Unknown')
    
    def _get_coordinates(self, city):
        """Retorna coordenadas aproximadas da cidade"""
        coordinates = {
            'São Paulo': (-23.5505, -46.6333),
            'Rio de Janeiro': (-22.9068, -43.1729),
            'New York': (40.7128, -74.0060),
            'Los Angeles': (34.0522, -118.2437),
            'Delhi': (28.6139, 77.2090),
            'Mumbai': (19.0760, 72.8777),
            'Beijing': (39.9042, 116.4074),
            'Shanghai': (31.2304, 121.4737),
            'Tokyo': (35.6762, 139.6503),
            'London': (51.5074, -0.1278)
        }
        return coordinates.get(city, (0, 0))
    
    def get_data(self, use_sample=True):
        """
        Método principal para obter dados
        
        Args:
            use_sample (bool): Se True, usa dados de exemplo
                               Se False, tenta baixar dados reais
        """
        print("=" * 60)
        print("🌍 COLETA DE DADOS - QUALIDADE DO AR")
        print("=" * 60)
        
        if not use_sample:
            success = self.download_from_kaggle()
            if success:
                # Encontrar arquivo baixado
                for file in os.listdir(self.raw_dir):
                    if file.endswith('.csv'):
                        filepath = os.path.join(self.raw_dir, file)
                        df = pd.read_csv(filepath, low_memory=False)
                        print(f"📄 Arquivo real carregado: {file}")
                        return df
        else:
            df = self.download_sample_data()
            return df

if __name__ == "__main__":
    # Testar o coletor de dados
    collector = DataCollector()
    df = collector.get_data(use_sample=True)
    
    print("\n📊 Estatísticas do dataset:")
    print(f"Total de registros: {len(df):,}")
    print(f"Cidades: {df['city'].unique().tolist()}")
    print(f"Poluentes: {df['parameter'].unique().tolist()}")
    print(f"Período: {df['date'].min()} a {df['date'].max()}")
    
    # Salvar informações
    info_path = os.path.join(collector.data_dir, 'dataset_info.txt')
    with open(info_path, 'w') as f:
        f.write(f"Dataset de Qualidade do Ar\n")
        f.write(f"Gerado em: {datetime.now()}\n")
        f.write(f"Total registros: {len(df):,}\n")
        f.write(f"Cidades: {', '.join(df['city'].unique())}\n")
        f.write(f"Poluentes: {', '.join(df['parameter'].unique())}\n")
    
    print(f"\n📝 Informações salvas em: {info_path}")