# Food Recall Search

This is a configuration of [search-a-licious](https://github.com/openfoodfacts/search-a-licious)
for Food Recall data.

## Start the service

You must have docker and docker compose installed.

Start the service:
```bash
docker compose up -d
```


## Importing the data

Get test data at https://drive.google.com/file/d/1iWpimLZ2XJTKDMA0pFbmY4KYbnAcMQoD/view?usp=share_link
or generate a fresh set using the notebooks in [`etl/`](../etl) folder.

copy in `data/recall_depart.jsonl`
and import them.

```bash
docker compose run --rm api python3 -m app import /opt/search/data/recall_depart.jsonl --skip-updates
```

## Use it

See the search service at http://search.localhost:8000/

Test the api: http://search.localhost:8000/docs
