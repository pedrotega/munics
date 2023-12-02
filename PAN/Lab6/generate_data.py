import numpy as np
import pandas as pd


def generate_dataset(n: int=200):
    '''
    Generates a toy dataset containing n distinct samples.

    - n: number of samples to generate

    Returns:
    - A tuple containing:
        * Dataset as a Pandas Dataframe
        * List of quasi-identifiers
        * Sensitive column name
    '''
    diseases = np.array(["Angine", "Appendicite", "Chlamydia", "Cataracte", "Dengue", 
                         "Eczéma", "Grippe", "Hépatite B", "Hépatite C", "Rhino-pharyngite", 
                         "Otite", "Rougeole", "Scarlatine", "Urticaire", "Varicelle", "Zona"])
    zipcodes = np.array([35000, 35200, 37000, 40000, 40500, 50000, 52000, 60000, 62000, 68000, 
                         75000, 75001, 75002, 75005])

    rows = []
    for _ in range(n):
        row = {'Age':np.random.randint(7, 77), 'ZipCode':np.random.choice(zipcodes), 'Disease':np.random.choice(diseases)}
        while row in rows:
            row = {'Age':np.random.randint(7, 77), 'ZipCode':np.random.choice(zipcodes), 'Disease':np.random.choice(diseases)}
        rows.append(row)
        
        
    dataset = pd.DataFrame(rows)
    dataset.sort_values(by = ['Age', 'ZipCode'], inplace=True)

    return dataset, ['Age', 'ZipCode'], 'Disease'