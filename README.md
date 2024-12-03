# Food recall

Making food products recall accessible to anyone. Help alerts reach public for more safety.


## Importing the data

From the json export.

1. put the data in `data/` eg. `rappelconso-v2-gtin-trie.json.gz`

2. import:
   ```bash
   docker compose run --rm api python3 -m app import /opt/search/data/rappelconso-v2-gtin-trie.json.gz --skip-updates
   ```

