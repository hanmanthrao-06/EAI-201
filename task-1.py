import pandas as pd
import json
import re
import numpy as np

def alpha_load_and_integration(csv_file, json_file):
    """
    Load and integrate zoo dataset with auxiliary metadata.
    Handles data cleaning, standardization, and missing value imputation.
    
    Parameters:
    -----------
    csv_file : str
        Path to the zoo.csv file
    json_file : str
        Path to the auxiliary_metadata.json file
    
    Returns:
    --------
    pd.DataFrame
        Merged and cleaned dataset with engineered features
    """
    
    # Step 1: Load and clean zoo CSV
    print("Step 1: Loading and cleaning zoo dataset...")
    zoo_df = pd.read_csv(csv_file)
    zoo_df['animal_name'] = zoo_df['animal_name'].apply(
        lambda x: re.sub(r'[^A-Za-z0-9]', '', str(x))
    )
    print(f"  ✓ Loaded {len(zoo_df)} animals from zoo dataset")
    
    # Step 2: Load and parse auxiliary metadata JSON
    print("\nStep 2: Loading and parsing auxiliary metadata...")
    with open(json_file, 'r') as f:
        aux_text = f.read()
    
    aux_data = []
    entries = re.findall(r'\{[^}]+\}', aux_text)
    for entry in entries:
        record = {}
        animal_match = re.search(r'"animal_name":\s*"([^"]+)"', entry)
        habitat_match = re.search(r'"habitat[s]?":\s*"([^"]+)"', entry)
        diet_match = re.search(r'"diet[_type]?":\s*"([^"]+)"', entry)
        conservation_match = re.search(
            r'"(?:conservation_status|conservation|status)":\s*"([^"]+)"', entry
        )
        
        if animal_match:
            record['animal_name'] = animal_match.group(1).strip()
        if habitat_match:
            record['habitat_type'] = habitat_match.group(1).strip()
        if diet_match:
            record['diet'] = d