"""
Módulo para limpeza e processamento de dados de qualidade do ar
"""
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class DataCleaner:
    """Classe para limpeza e processamento de dados"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.cleaned_df = None
    
    def clean_data(self):
        """Pipeline completo de limpeza"""
        print("🧹 Iniciando limpeza de dados...")
        
        # 1. Converter tipos
        self._convert_dtypes()
        
        # 2. Remover duplicatas
        self._remove_duplicates()
        
        # 3. Tratar valores ausentes
        self._handle_missing_values()
        
        # 4. Criar features
        self._create_time_features()
        
        # 5. Validar
        self._validate_data()
        
        self.cleaned_df = self.df
        print(f"✅ Limpeza concluída! Registros: {len(self.cleaned_df):,}")
        
        return self.cleaned_df
    
    def _convert_dtypes(self):
        """Converte tipos de dados"""
        print("  🔄 Convertendo tipos de dados...")
        
        if 'date' in self.df.columns:
            self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
        
        if 'value' in self.df.columns:
            self.df['value'] = pd.to_numeric(self.df['value'], errors='coerce')
    
    def _remove_duplicates(self):
        """Remove registros duplicados de forma segura"""
        initial_count = len(self.df)
        
        # Verificar colunas disponíveis
        available_cols = list(self.df.columns)
        print(f"  🔍 Colunas disponíveis: {available_cols}")
        
        # Definir colunas para identificar duplicatas
        possible_cols = ['date', 'city', 'parameter', 'value', 'latitude', 'longitude']
        
        # Usar apenas colunas que existem
        use_cols = [col for col in possible_cols if col in self.df.columns]
        
        if len(use_cols) >= 2:
            print(f"  🗑️  Removendo duplicatas usando: {use_cols}")
            self.df = self.df.drop_duplicates(subset=use_cols, keep='first')
        else:
            print("  ⚠️  Poucas colunas para verificar duplicatas")
        
        removed = initial_count - len(self.df)
        if removed > 0:
            print(f"    Removidos {removed} duplicatas")
    
    def _handle_missing_values(self):
        """Trata valores ausentes"""
        print("  🔍 Tratando valores ausentes...")
        
        missing_before = self.df.isnull().sum().sum()
        
        # Remover linhas sem dados essenciais
        essential = ['date', 'city', 'parameter']
        essential = [col for col in essential if col in self.df.columns]
        
        if essential:
            self.df = self.df.dropna(subset=essential)
        
        # Imputar valores ausentes
        if 'value' in self.df.columns:
            # Preencher com média por cidade e poluente
            self.df['value'] = self.df.groupby(['city', 'parameter'])['value'].transform(
                lambda x: x.fillna(x.mean())
            )
        
        missing_after = self.df.isnull().sum().sum()
        print(f"    Valores ausentes: {missing_before} → {missing_after}")
    
    def _create_time_features(self):
        """Cria features temporais"""
        print("  ⏰ Criando features temporais...")
        
        if 'date' in self.df.columns:
            self.df['year'] = self.df['date'].dt.year
            self.df['month'] = self.df['date'].dt.month
            self.df['day_of_week'] = self.df['date'].dt.dayofweek
            self.df['is_weekend'] = self.df['day_of_week'].isin([5, 6]).astype(int)
            
            # Estações do ano
            self.df['season'] = self.df['month'].apply(self._get_season)
    
    def _get_season(self, month):
        """Determina a estação do ano"""
        if month in [12, 1, 2]:
            return 'Verão'
        elif month in [3, 4, 5]:
            return 'Outono'
        elif month in [6, 7, 8]:
            return 'Inverno'
        else:
            return 'Primavera'
    
    def _validate_data(self):
        """Validação final"""
        print("  ✅ Validando dados...")
        
        if len(self.df) == 0:
            raise ValueError("Nenhum dado restante!")
        
        print(f"    📈 Dimensões: {self.df.shape}")
        print(f"    📅 Período: {self.df['date'].min()} a {self.df['date'].max()}")
    
    def save_cleaned_data(self, filepath='data/processed/cleaned_data.csv'):
        """Salva os dados limpos"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        self.cleaned_df.to_csv(filepath, index=False)
        print(f"💾 Dados salvos: {filepath}")
        
        return filepath

def clean_air_quality_data(df, save_path='data/processed/'):
    """Função principal para limpeza"""
    import os
    
    cleaner = DataCleaner(df)
    cleaned_data = cleaner.clean_data()
    
    if save_path:
        os.makedirs(save_path, exist_ok=True)
        output_file = os.path.join(save_path, 'cleaned_data.csv')
        cleaner.save_cleaned_data(output_file)
    
    return cleaned_data

if __name__ == "__main__":
    # Teste
    print("🧪 Testando limpeza...")
    
    test_data = pd.DataFrame({
        'date': pd.date_range('2023-01-01', periods=100, freq='D'),
        'city': ['São Paulo'] * 100,
        'parameter': ['PM2.5'] * 100,
        'value': np.random.normal(30, 10, 100)
    })
    
    cleaned = clean_air_quality_data(test_data, save_path=None)
    print(f"✅ Teste OK! Dados: {len(cleaned)} registros")