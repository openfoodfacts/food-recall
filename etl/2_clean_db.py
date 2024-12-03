#%%
import pandas as pd
import geopandas as gpd
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

departments = gpd.read_file('etl/input/departements.geojson')

# create a list with all departments
departments_list = list(departments['code'])

# if department is an empty list, replace it with departements_list
df_recall_depart['department'] = df_recall_depart['department'].apply(lambda x: x if x else departments_list)

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

# # Merge the dataframes
# departments = departments.merge(df_recall_depart.groupby('department').size().reset_index(name='recalls'),
#                                 left_on='code', right_on='department')
#
# # Plot the map
# fig, ax = plt.subplots(1, 1, figsize=(10, 10))
# departments.plot(column='recalls', ax=ax, legend=True)
# plt.show()

#%%
# Focus on the risques_encourus

# Get the count of risques_encourus
risques_encourus = df_recall_depart['risques_encourus'].value_counts()

# Classify the risques_encourus into 3 categories: 'biological', 'chemical', 'physical'
# Create a dictionnary with key words to map

key_words = {'bilogical': ['virus', 'bact', 'parasite', 'micro', 'botulis',
                           'biologique', 'biological', 'listeria', 'salmonella', 'coli', 'norovirus'],
             'allergen': ['allergen', 'allergène', 'allergi'],
             'chemical': ['pesticide', 'contaminant', 'mycotoxin', 'residue', 'contamination', 'oxyde'],
             'physical': ['verre', 'plastic', 'foreign', 'metal', 'blessure'],
             'labelling (other)': ['etiqueta', 'label', 'etiquetage', 'etiquette', 'étiquetage']}

# Create a function to classify the risques_encourus
def classify_risque(risque):
    for key, values in key_words.items():
        for value in values:
            if value in risque.lower():
                return key
    return 'other'


df_recall_depart['risques_encourus_tot'] = df_recall_depart['risques_encourus'] + ' ' + df_recall_depart['motif_rappel']

# Apply the function to the risques_encourus column
df_recall_depart['risque_class'] = df_recall_depart['risques_encourus_tot'].apply(classify_risque)

# delete the risques_encourus_tot column
df_recall_depart.drop(columns=['risques_encourus_tot'], inplace=True)

# Save file to jsonl
# df_recall_depart['key'] = df_recall_depart['gtin'] + '--' + df_recall_depart['id']
df_recall_depart.to_json('etl/output/recall_depart.jsonl', orient='records', lines=True)

#%%
import matplotlib.pyplot as plt
# Visualize the data on a map
# Explode per department
df_recall_depart = df_recall_depart.explode('department')

# Merge the dataframes
departments_plot = departments.merge(df_recall_depart.groupby('department').size().reset_index(name='recalls'),
                                left_on='code', right_on='department')

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
departments_plot.plot(column='recalls', ax=ax, legend=True)

# Save the plot
plt.savefig('etl/output/recalls_per_department.png')
plt.show()

#%%
# Get the count per zone_geographique
geography_summary = df_recall_depart.groupby('zone_geographique_de_vente').size().reset_index(name='recalls')

# Get the count per risque_class
risque_summary = df_recall_depart.groupby('risque_class').size().reset_index(name='recalls')