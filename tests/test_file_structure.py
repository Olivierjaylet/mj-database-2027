import pandas as pd
import pytest
required_files = ['candidates.csv', 
                      'polls.csv', 
                      'poll_types.csv'
                      ]

def test_csv_files_exist():
    
    for file in required_files:
        assert pd.read_csv(file) is not None, f"Fichier {file} manquant ou invalide"

def test_csv_encoding():

    for file in required_files:
        with open(file, 'rb') as f:
            assert 'utf-8' in str(f.read(1000).decode('utf-8', errors='ignore'))
