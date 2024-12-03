# Food Recall Search

This is a configuration of [search-a-licious](https://github.com/openfoodfacts/search-a-licious)
for Food Recall data.

To test it:

Start the service:
```bash
docker compose up -d
```

Get test data at https://drive.google.com/file/d/1iWpimLZ2XJTKDMA0pFbmY4KYbnAcMQoD/view?usp=share_link

Import the data

```bash
docker compose run --rm api python3 -m app import /opt/search/data/recall_depart.jsonl --skip-updates
```

See the search service at http://search.localhost:8000/

Test the api http://search.localhost:8000/docs
