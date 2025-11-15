import pandas as pd
import re

print("\n" + "="*70)
print("ALPHA LOAD AND INTEGRATION - TASK 1")
print("="*70 + "\n")

# STEP 1
print("[STEP 1] Loading zoo.csv...")
zoo_df = pd.read_csv('zoo.csv')
print(f"OK: {len(zoo_df)} animals loaded\n")

# STEP 2
print("[STEP 2] Cleaning animal names...")
zoo_df['animal_name'] = zoo_df['animal_name'].apply(lambda x: re.sub(r'[^A-Za-z0-9]', '', str(x)))
print(f"OK: Names cleaned\n")

# STEP 3
print("[STEP 3] Loading auxiliary_metadata.json...")
with open('auxiliary_metadata.json', 'r') as f:
    aux_text = f.read()
print(f"OK: File loaded\n")

# STEP 4
print("[STEP 4] Parsing JSON...")
aux_data = []
entries = re.findall(r'\{[^}]+\}', aux_text)
print(f"OK: {len(entries)} records found\n")

for entry in entries:
    record = {}
    animal_match = re.search(r'"animal_name":\s*"([^"]+)"', entry)
    habitat_match = re.search(r'"habitat[s]?":\s*"([^"]+)"', entry)
    diet_match = re.search(r'"diet[_type]?":\s*"([^"]+)"', entry)
    conservation_match = re.search(r'"(?:conservation_status|conservation|status)":\s*"([^"]+)"', entry)
    
    if animal_match:
        record['animal_name'] = animal_match.group(1).strip()
    if habitat_match:
        record['habitat_type'] = habitat_match.group(1).strip()
    if diet_match:
        record['diet'] = diet_match.group(1).strip()
    if conservation_match:
        record['conservation_status'] = conservation_match.group(1).strip()
    
    if record.get('animal_name'):
        aux_data.append(record)

# STEP 5
print("[STEP 5] Standardizing...")
fixed_diets = {
    'omnivor': 'omnivore',
    'herbivor': 'herbivore',
    'carnivore': 'carnivore',
    'herbivore': 'herbivore',
    'omnivore': 'omnivore',
    'insectivore': 'insectivore',
    'filterfeeder': 'filter feeder'
}

habitat_map = {
    'fresh water': 'freshwater',
    'freshwater': 'freshwater',
    'marinecoastal': 'marine coastal',
    'marine': 'marine',
    'forest': 'forest',
    'grasslands': 'grasslands',
    'savanna': 'savanna',
    'domestic': 'domestic'
}

standardized_aux = []
for record in aux_data:
    new_record = {}
    for key, value in record.items():
        if key == 'animal_name':
            new_record['animal_name'] = re.sub(r'[^a-z0-9]', '', value.lower())
        elif key == 'habitat_type':
            new_record['habitat_type'] = habitat_map.get(value.lower(), value.lower())
        elif key == 'diet':
            new_record['diet'] = fixed_diets.get(value.lower(), value.lower())
        else:
            new_record[key] = value.lower()
    standardized_aux.append(new_record)

aux_df = pd.DataFrame(standardized_aux)
print(f"OK: {len(standardized_aux)} records standardized\n")

# STEP 6
print("[STEP 6] Merging...")
merged_df = pd.merge(zoo_df, aux_df, on='animal_name', how='left')
print(f"OK: {len(merged_df)} total, {len(aux_df)} with auxiliary\n")

# STEP 7
print("[STEP 7] Filling missing values...")
for col in ['habitat_type', 'diet', 'conservation_status']:
    missing = merged_df[col].isnull().sum()
    if missing > 0:
        mode_val = merged_df[col].mode()[0]
        merged_df[col] = merged_df[col].fillna(mode_val)
        print(f"OK: {col} - {missing} filled with '{mode_val}'")
print()

# STEP 8
print("[STEP 8] Feature engineering...")

def is_endangered(x):
    if pd.isna(x):
        return 0
    return 1 if any(s in str(x).lower() for s in ['vulnerable', 'endangered', 'critically']) else 0

def complexity(x):
    m = {'carnivore': 3, 'omnivore': 2, 'herbivore': 1, 'insectivore': 1, 'filter feeder': 1}
    if pd.isna(x):
        return 0
    return m.get(str(x).lower(), 0)

merged_df['is_endangered'] = merged_df['conservation_status'].apply(is_endangered)
merged_df['diet_complexity'] = merged_df['diet'].apply(complexity)
print(f"OK: is_endangered created ({merged_df['is_endangered'].sum()} found)")
print(f"OK: diet_complexity created\n")

# STEP 9
print("[STEP 9] Saving...")
merged_df.to_csv('merged_zoo_data_with_features.csv', index=False)
print(f"OK: Saved\n")

# SUMMARY
print("="*70)
print("FINAL RESULTS")
print("="*70)
print(f"Total records: {len(merged_df)}")
print(f"Total features: {len(merged_df.columns)}")
print(f"\nEndangered animals: {merged_df['is_endangered'].sum()}")
for animal in merged_df[merged_df['is_endangered']==1]['animal_name'].values:
    print(f"  - {animal}")

print(f"\nDiet Complexity Distribution:")
for c in sorted(merged_df['diet_complexity'].unique()):
    cnt = (merged_df['diet_complexity'] == c).sum()
    print(f"  Level {int(c)}: {cnt} animals")

print(f"\nSample Data (first 5):")
print(merged_df[['animal_name', 'diet', 'conservation_status', 'is_endangered', 'diet_complexity']].head(5).to_string())
print("\n" + "="*70)
print("SUCCESS - TASK COMPLETE")
print("="*70 + "\n")
