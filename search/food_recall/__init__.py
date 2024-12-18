from app.indexing import BaseDocumentPreprocessor
from app._import import BaseDocumentFetcher

from app._types import FetcherResult, FetcherStatus, JSONType


class RappelConsoPreprocessor(BaseDocumentPreprocessor):
    """a preprocessor for RappelConso (french) data"""

    # gtin, numero_fiche, numero_version, nature_juridique_rappel, categorie_produit, sous_categorie_produit, marque_produit, 
    # modeles_ou_references, identification_produits, conditionnements, date_debut_commercialisation,
    # date_date_fin_commercialisation, temperature_conservation, marque_salubrite, informations_complementaires, 
    # zone_geographique_de_vente, distributeurs, motif_rappel, risques_encourus, preconisations_sanitaires, 
    # description_complementaire_risque, conduites_a_tenir_par_le_consommateur, numero_contact, modalites_de_compensation,
    # date_de_fin_de_la_procedure_de_rappel, informations_complementaires_publiques, liens_vers_les_images,
    # lien_vers_la_liste_des_produits, lien_vers_la_liste_des_distributeurs, lien_vers_affichette_pdf,
    # lien_vers_la_fiche_rappel, rappel_guid, date_publication, libelle, id
    FIELD_TRANSLATION = {
        "original_id": "id",
        "version": "numero_version",
        "barcode": "gtin",
        "title": "modeles_ou_references",
        "off_title": "off_product_name",
        "publication_date": "date_publication",
        "original_link": "lien_vers_la_fiche_rappel",
        "sold_start": "date_debut_commercialisation",
        "sold_end": "date_date_fin_commercialisation",
        "geography_text": "zone_geographique_de_vente",
        "geo_district": "department",
        "retailers_text": "distributeurs",
        "category": "categorie_produit",
        "sub_category": "sous_categorie_produit",
        "off_brands_tags": "off_brands_tags",
        "off_categories_tags": "off_categories_tags",
        "brands_text": "marque_produit",
        "references": "modeles_ou_references",
        "identification": "identification_produits",
        "conditioning": "conditionnements",
        "images": "liens_vers_les_images",
        "risk_class": "risque_class",
        "off_code": "off_code",
    }
    DATE_FIELDS = ["publication_date", "sold_start", "sold_end"]

    def _normalize_date(self, date):
        # we jut need to add the T instead of the space
        return date.replace(' ', 'T')

    def split_list(self, data, sep="|"):
        return [d.strip().lower() for d in data.split(sep)] if data is not None else None

    def replace_bad_chars(self, data, *fields):
        for field in fields:
            if data.get("field"):
                data[field] = data[field].replace("¤", ",")

    def preprocess(self, document: JSONType) -> FetcherResult:
        # no need to have a deep-copy here
        new_document: JSONType = {
            new_key: document[orig_key]
            for new_key, orig_key in self.FIELD_TRANSLATION.items()
        }
        # build a unique id
        new_document["recall_id"] = f"{new_document['original_id']}--{new_document['barcode']}"
        new_document["source"] = "rappelconso"
        new_document["original_link"] = f"https://rappel.conso.gouv.fr/fiche-rappel/{new_document['original_id']}/Interne"
        # normalize dates
        for date_field in self.DATE_FIELDS:
            if new_document[date_field] is not None:
                new_document[date_field] = self._normalize_date(new_document[date_field])
        self.replace_bad_chars(new_document, "brands_text", "retailers_text", "title")
        # brands is a list
        new_document["brands"] = self.split_list(new_document["brands_text"], ",")
        new_document["retailers"] = self.split_list(new_document["retailers_text"], ",")
        # some lists
        new_document["images"] = self.split_list(new_document["images"])
        return FetcherResult(status=FetcherStatus.FOUND, document=new_document)


class RappelConsoFetcher(BaseDocumentFetcher):
    """a fetcher for RappelConso (french) data"""

    def fetch_document(self, stream_name: str, item: JSONType) -> FetcherResult:
        return FetcherResult(status=FetcherStatus.SKIP, document=None)
