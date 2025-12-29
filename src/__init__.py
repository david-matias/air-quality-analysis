"""
Módulo de análise de qualidade do ar
"""
__version__ = "1.0.0"
__author__ = "David Matias"
__email__ = "davidmatias8@gmail.com"

from .data_collection import DataCollector
from .data_cleaning import DataCleaner, clean_air_quality_data
from .dashboard import AirQualityDashboard
from .pipeline import run_full_pipeline

__all__ = [
    'DataCollector',
    'DataCleaner',
    'clean_air_quality_data',
    'AirQualityDashboard',
    'run_full_pipeline'
]