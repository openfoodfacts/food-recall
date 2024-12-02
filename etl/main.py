import pandas as pd
import requests
from gtin.validator import *
#%%
input_url = 'https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/rappelconso-v2-gtin-trie/exports/json?lang=fr&timezone=Europe%2FBerlin'
# Download the json file to the input folder

response = requests.get(input_url)
#%%
with open('etl/input/recall.json', 'wb') as f:
    f.write(response.content)
#%%

# Load the json file to a dataframe

df_recall = pd.read_json('etl/input/recall.json')
#%%
# Add a column to the dataframe to check if the GTIN is valid
df_recall['gtin_valid'] = df_recall['gtin'].apply(is_valid_GTIN)
