import os
import pandas as pd

def test_poll_filename_format():

    poll_files = os.listdir('polls/')

    for file in poll_files:

        assert '_' in file, f"Nom de fichier invalide : {file}"
        
        assert file.endswith('.csv'), f"Extension invalide : {file}"

def test_poll_references_valid_candidates():

    candidates = pd.read_csv('candidates.csv')['acronyme'].tolist()

    for file in os.listdir('polls/'):

        df = pd.read_csv(f'polls/{file}')

        for candidate in df['candidate']:
            assert candidate in candidates, f"Candidat invalide dans {file} : {candidate}"