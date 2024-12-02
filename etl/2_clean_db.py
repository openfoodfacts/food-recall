#%%
import pandas as pd

# Load the data
df_recall_alim = pd.read_csv('etl/output/recall_alim.csv')
#%%
df_recall_depart = df_recall_alim.copy()
# Extract department from zone_geographique_de_vente columns
# df_recall_depart['department'] = df_recall_depart['zone_geographique_de_vente'].str.extract(r'(\d{2})')
df_recall_depart = df_recall_depart.assign(department=df_recall_depart['zone_geographique_de_vente'].str.findall(r'(\d{2})')).explode('department')
# Remove the rows where the department is not valid
df_recall_depart = df_recall_depart[df_recall_depart['department'].notna()]
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
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-mpnet-base-v2')

name = 'ile de france'
q_embedding = model.encode([name])
# d_embeddings = model.encode(list(departments['nom']))


#%%
def find_best_match(name):
    # Find the best match
    q_embedding = model.encode([name])
    d_embeddings = model.encode(list(departments['nom']))
    scores = (d_embeddings @ q_embedding.T).flatten()
    matches = scores.argsort()[::-1]
    # Get the best match
    best_match = departments.iloc[matches[1:].argmax()]['nom']
    return best_match

find_best_match('Paris')

#%%


# Create a dataframe with the number of recalls per depar

# Merge the dataframes
departments = departments.merge(df_recall_depart.groupby('department').size().reset_index(name='recalls'),
                                left_on='code', right_on='department')

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
departments.plot(column='recalls', ax=ax, legend=True)
plt.show()

