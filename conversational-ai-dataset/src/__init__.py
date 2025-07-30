"""
Conversational AI Dataset Package

A comprehensive toolkit for creating, analyzing, and preparing conversational datasets
for training transformer-based AI models.
"""

__version__ = "1.0.0"
__author__ = "Adrian Paredez"
__description__ = "High-quality conversational dataset for training AI models"

from .tools import dataset_analyzer, data_preprocessor
from .utils import *

__all__ = [
    "dataset_analyzer",
    "data_preprocessor",
]
