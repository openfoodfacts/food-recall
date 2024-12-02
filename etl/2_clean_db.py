#%%
import pandas as pd

# Load the data
df_recall_alim = pd.read_csv('etl/output/recall_alim.csv')
#%%
df_recall_depart = df_recall_alim.copy()
# Extract department from zone_geographique_de_vente columns
# df_recall_depart['department'] = df_recall_depart['zone_geographique_de_vente'].str.extract(r'(\d{2})')
# df_recall_depart = df_recall_depart.assign(department=df_recall_depart['zone_geographique_de_vente'].str.findall(r'(\d{2})')).explode('department')

import re

# Function to convert digits longer than 2 into 2 digits
def convert_to_two_digits(text):
    return re.sub(r'(\d{2})\d+', r'\1', text)

# Apply the function to the 'zone_geographique_de_vente' column
df_recall_depart['zone_geographique_de_vente'] = df_recall_depart['zone_geographique_de_vente'].apply(convert_to_two_digits)
df_recall_depart = df_recall_depart.assign(department=df_recall_depart['zone_geographique_de_vente'].str.findall(r'(\d{2})'))
#
# df_recall_depart = df_recall_depart.assign(
#     department=df_recall_depart['zone_geographique_de_vente'].str.findall(r'(\d{2,})').apply(lambda x: x[0][:2] if x else None)
# )

# Remove the rows where the department is not valid
# df_recall_depart = df_recall_depart[df_recall_depart['department'].notna()]

# Save the dataframe to a csv file
df_recall_depart.to_csv('etl/output/recall_depart.csv', index=False)

# Export to Json
df_recall_depart.to_json('etl/output/recall_depart.json', orient='records')

#%%
# Plot the number of recalls per department on a map
import geopandas as gpd
import matplotlib.pyplot as plt

# Load the departments shapefile
departments = gpd.read_file('etl/input/departements.geojson')

# if department is not found, find the best match of zone_geographique_de_vente with the department name
# Use sentence transformer to find the best match

#%%
# Create a function to find the best match
# from sentence_transformers import SentenceTransformer
# model = SentenceTransformer('all-mpnet-base-v2')
#
# d_embeddings = model.encode(list(departments['nom']))

#%%
# def find_best_match(name, threshold=0.8):
#     # Find the best match
#     q_embedding = model.encode([name])
#     scores = (d_embeddings @ q_embedding.T).flatten()
#     matches = scores.argsort()[::-1]
#     match_score = scores[matches[0]]
#     # Get the match with the highest score
#     best_match = departments.iloc[matches[0]]['code']
#
#     if match_score < threshold:
#         return None, None
#     return best_match, match_score
#
#
# find_best_match('Savoua')

#%%
# on df_recall_depart, if department is not found, find the best match of zone_geographique_de_vente with the department name
# Use sentence transformer to find the best match

# df_recall_depart['department'] = df_recall_depart.apply(lambda x: find_best_match(x.zone_geographique_de_vente)[0] if pd.isna(x['department']) else x['department'], axis=1)
#
# for index, row in df_recall_depart.iterrows():
#     if pd.isna(row['department']):
#         best_match, _ = find_best_match(row['zone_geographique_de_vente'])
#         df_recall_depart.at[index, 'department'] = best_match

#%%


# Create a dataframe with the number of recalls per depar

# Merge the dataframes
departments = departments.merge(df_recall_depart.groupby('department').size().reset_index(name='recalls'),
                                left_on='code', right_on='department')

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
departments.plot(column='recalls', ax=ax, legend=True)
plt.show()

