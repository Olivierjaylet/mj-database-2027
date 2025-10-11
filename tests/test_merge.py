import pandas as pd
import pytest

import os

import subprocess
import tempfile
import shutil



def test_poll_mergeable_with_main():
    """Vérifie que le nouveau sondage peut être fusionné avec merge.py"""
    
    # Copie le repo dans un dossier temporaire
    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree('.', 
                        temp_dir, 
                        dirs_exist_ok=True
                        )
        
        # Tenter d'exécuter merge.py
        result = subprocess.run(
            ['python', 'merge.py'], 
            cwd=temp_dir, 
            capture_output=True, 
            text=True
        )
        
        assert result.returncode == 0, f"merge.py a échoué: {result.stderr}"
        
        # Vérifier que les fichiers de sortie sont créés
        expected_files = ['mj2027.csv', 
                          'mj2027_left.csv', 
                          'mj2027_farright.csv', 
                         'mj2027_macron.csv', 
                         'mj2027_absentionists.csv'
                         ]
        
        for file in expected_files:
            assert os.path.exists(os.path.join(temp_dir, file))

def test_poll_data_consistency_after_merge():
    """Vérifie la cohérence des données après merging"""

    with tempfile.TemporaryDirectory() as temp_dir:
        shutil.copytree('.', 
                        temp_dir, 
                        dirs_exist_ok=True
                        )

        # Exécuter merge.py
        subprocess.run(['python',
                        'merge.py'],
                        cwd=temp_dir,
                        check=True
                        )
        

        expected_columns_dic = {
            "full": [
                'candidate_id', 'intention_mention_1', 'intention_mention_2', 'intention_mention_3',
                'intention_mention_4', 'intention_mention_5', 'intention_mention_6', 'intention_mention_7',
                'poll_type_id', 'population', 'poll_id', 'poll_type', 'nb_people', 'start_date',
                'end_date', 'folder', 'id', 'institut', 'commanditaire', 'mention1', 'mention2',
                'mention3', 'mention4', 'mention5', 'mention6', 'mention7', 'nombre_mentions',
                'question', 'name', 'surname', 'parti', 'annonce_candidature', 'retrait_candidature',
                'second_round', 'candidate'
            ],
            "restricted": [
                'candidate_id', 'intention_mention_1', 'intention_mention_2', 'intention_mention_3',
                'poll_type_id', 'population', 'poll_id', 'poll_type', 'nb_people', 'start_date',
                'end_date', 'folder', 'id', 'institut', 'commanditaire', 'mention1', 'mention2',
                'mention3', 'nombre_mentions', 'question', 'name', 'surname', 'parti',
                'annonce_candidature', 'retrait_candidature', 'second_round'
            ]
        }

        # Liste des fichiers générés à vérifier
        files = [
            'mj2027.csv',
            'mj2027_left.csv',
            'mj2027_farright.csv',
            'mj2027_macron.csv',
            'mj2027_absentionists.csv'
        ]

        # Charger la liste des candidats valides
        candidates = pd.read_csv(os.path.join(temp_dir, 'candidates.csv'))['candidate_id'].tolist()

        for file in files:
            file_path = os.path.join(temp_dir, file)

            if not os.path.exists(file_path):
                                print(f"⚠️ {file} n'existe pas.")
                                continue  # Passe au fichier suivant
            
            # Charger le fichier
            df = pd.read_csv(file_path)

            # Verifie que le fichier n'est pas vide
            assert not df.empty, f"Fichier vide : {file}"

            # verifie que toutes les references aux candidats sont valides
            for candidate_id in df['candidate_id']:
                assert candidate_id in candidates, \
                    f"Candidat invalide '{candidate_id}' détecté dans {file}"

            # verifie si des doublons existent
            assert df.duplicated().any() == False, \
                f"Des doublons ont été détectés dans {file}"
            
            # Prend l'une des liste de colonnes
            if file == 'mj2027.csv' :
                expected_columns =  expected_columns_dic['full']  
            
            else :
                  expected_columns = expected_columns_dic['restricted']
            
            # verifie si toutes les colonnes existent encore
            missing_columns = [col for col in expected_columns if col not in df.columns]

            if missing_columns:
                assert False, f"Colonnes manquantes dans {file_path} : {missing_columns}"

            assert set(expected_columns).issubset(df.columns), (
                f"Missing columns in {file_path}: {sorted(set(expected_columns) - set(df.columns))}"
            )

            # verifie s'il y a plus de colonne que prevu
            extra_columns = set(df.columns) - set(expected_columns)
            assert not extra_columns, f"Extra columns in {file_path}: {sorted(extra_columns)}"
            
            print(f"✅ {file} est valide.")