# Exploration with datasette

[Datasette](https://datasette.io/) is a very cool tool "for exploring and publishing data. It helps people take data of any shape, analyze and explore it, and publish it as an interactive website and accompanying API".

## Exploration

During the 2024's hackathon in Paris, the DGCCRF has provided a CSV to beta-test the evolution of their dataset.

Thanks to [csv2datasette](https://gist.github.com/CharlesNepote/3fdb8982dc873f34aa7c320bef580fe3), we can directly visualize and explore this CSV file. csv2datasette is a bash script which open CSV files directly in Datasette. It offers a number of options for reading and exploring CSV files, such as `--stats`, inspired by [WTFCsv](https://www.databasic.io/en/wtfcsv/).

`--stats` option includes, for each column: the column name, the number of unique values, the number of filled rows, the number of missing values, the mininmum value, the maximum value, the median, the 10th, 25th, 50th, 75th and 90th centiles, the average, the sum, the shortest string, the longest string, the number of numeric values, the number of text values, the number of probable ISO dates, the top 3 frequent values.

if you want to try it with the given CSV, you also have to deal with the "French" CSV, which means using ";" as column separators. This command line will do the trick:
```bash
csv2datasette.sh --stats -s ";" rappelconso-v2-gtin-trie.csv
```

If you're lazy, and you don't want to install datasette, you can just reuse the database on Mirabelle platform:
https://mirabelle.openfoodfacts.org/rappelconso_v2_gtin_trie

## JSON API

Datasette automagically builds a JSON API. The documentation is here: https://docs.datasette.io/en/stable/json_api.html

Example, if you want to request a specific product:
Example https://mirabelle.openfoodfacts.org/rappelconso_v2_gtin_trie/rappelconso_v2_gtin_trie.json?_sort=rowid&%EF%BB%BFgtin__exact=3760289220694&_shape=array 

You'll get a nice json like this:
```json
[
  {
    "rowid": 1,
    "﻿gtin": "3760289220694",
    "﻿numero_fiche": "2021-05-0242",
    "numero_version": "1",
    "nature_juridique_rappel": "volontaire (sans arrêté préfectoral)",
    "categorie_produit": "alimentation",
    "sous_categorie_produit": "aliments diététiques et nutrition",
    "marque_produit": "keto slim nuit",
    "modeles_ou_references": "keto slim nuit¤¤pack keto",
    "identification_produits": "3760289220694$ken134f$non concerné$$|3760289220748$ken134f$non concerné$$",
    "conditionnements": "keto slim nuit : boite en carton de 3 blisters de 20 gélules soit 60 gélules (poids net de 41g).¤pack keto : valisette en carton avec 3 produits et le keto slim nuit avec le lot ken134f",
    "date_debut_commercialisation": "2020-06-30T00:00:00+00:00",
    "date_date_fin_commercialisation": "2021-04-20T00:00:00+00:00",
    "temperature_conservation": "produit à conserver à température ambiante",
    "marque_salubrite": "",
    "informations_complementaires": "",
    "zone_geographique_de_vente": "france entière",
    "distributeurs": "pharmacies, parapharmacies indépendantes et gms (galec, carrefour, auchan, système u).",
    "motif_rappel": "présence d'oxyde d'éthylène à une teneur supérieure à la législation européenne.",
    "risques_encourus": "dépassement des limites autorisées de pesticides",
    "preconisations_sanitaires": "",
    "description_complementaire_risque": "",
    "conduites_a_tenir_par_le_consommateur": "ne plus consommer|rapporter le produit au point de vente|contacter le service consommateur",
    "numero_contact": "0800808909",
    "modalites_de_compensation": "remboursement|echange",
    "date_de_fin_de_la_procedure_de_rappel": "2021-06-30T00:00:00+00:00",
    "informations_complementaires_publiques": "",
    "liens_vers_les_images": "https://rappel.conso.gouv.fr/image/df223eec-c212-416c-9612-e0f39263f022.jpg|https://rappel.conso.gouv.fr/image/7af06118-0f66-4156-8e65-dada671bce9f.jpg",
    "lien_vers_la_liste_des_produits": "",
    "lien_vers_la_liste_des_distributeurs": "https://rappel.conso.gouv.fr/document/58fe3fd8-fb33-43cb-a872-750afbd17e53/interne/listedesdistributeurs",
    "lien_vers_affichette_pdf": "https://rappel.conso.gouv.fr/affichettepdf/556/interne",
    "lien_vers_la_fiche_rappel": "https://rappel.conso.gouv.fr/fiche-rappel/556/interne",
    "rappel_guid": "d424350b-b498-4c97-8fa3-682463dc64a8",
    "date_publication": "2021-06-01T15:04:00+00:00",
    "libelle": "keto slim nuit",
    "id": "556"
  }
]
```

