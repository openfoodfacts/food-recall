import pandas as pd
import requests
from gtin.validator import *

#%%
sample = None
input_url = 'https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/rappelconso-v2-gtin-trie/exports/json?lang=fr&timezone=Europe%2FBerlin'
# Download the json file to the input folder
#%%
response = requests.get(input_url)
#%%
with open('etl/input/recall.json', 'wb') as f:
    f.write(response.content)
#%%
# Read off data
df_off = pd.read_csv('etl/input/en.openfoodfacts.org.products.csv',
                     usecols=['code', 'product_name', 'brands_tags', 'categories_tags', 'allergens'],
                     sep='\t', encoding='utf-8', on_bad_lines='skip', nrows=sample)
#%%
df_off['off_code'] = df_off['code']
df_off.rename(columns={'code': 'gtin'}, inplace=True)

# df_off['gtin_valid'] = df_off['gtin'].apply(is_valid_GTIN)
# Remove the rows where the gtin is not valid
# df_off = df_off[df_off['gtin_valid'] == True]
# Drop the gtin_valid column
# df_off.drop(columns=['gtin_valid'], inplace=True)

#%%
# Change the gtin column to int
df_off['gtin'] = df_off['gtin'].astype(str)
# zfill the gtin column with 13 digits
df_off['gtin'] = df_off['gtin'].str.zfill(13)
#%%
# Load the json file to a dataframe
df_recall = pd.read_json('etl/input/recall.json')
#%%
# Add a column to the dataframe to check if the GTIN is valid
df_recall['gtin_valid'] = df_recall['gtin'].apply(is_valid_GTIN)
df_recall['gtin'] = df_recall['gtin'].astype(str)
df_recall['gtin'] = df_recall['gtin'].str.zfill(13)
# Filter OFF data with GTIN from recall data
df_off = df_off[df_off['gtin'].isin(df_recall['gtin'])]


#%%
# Create a function to check if the GTIN is in the open food facts database, and add product name
# def get_product_name(gtin):
#     try:
#         return df_off[df_off['gtin'] == gtin]['product_name'].values[0]
#     except:
#         return None

# Merge the dataframes
df_recall = df_recall.merge(df_off, on='gtin', how='left')

# Add a column to the dataframe to get the product name
# df_recall['off_product_name'] = df_recall['gtin'].apply(get_product_name)

#%%
# Get some statistics
df_recall_alim = df_recall[df_recall['categorie_produit'] == 'alimentation']
df_recall_alim = df_recall_alim[df_recall_alim['gtin_valid'] == True]

df_recall_alim.rename(columns={'brands_tags': 'off_brands_tags',
                               'product_name': 'off_product_name',
                               'allergens': 'off_allergens',
                               'categories_tags': 'off_categories_tags'}, inplace=True)

#%%
# Save the dataframe to a csv file
df_recall_alim.to_csv('etl/output/recall_alim.csv', index=False)
