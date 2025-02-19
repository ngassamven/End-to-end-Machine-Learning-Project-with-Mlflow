import os
import urllib.request as request
import zipfile
from mlProject import logger
from mlProject.utils.common import get_size
from pathlib import Path
from mlProject.entity.config_entity import DataIngestionConfig



class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        """Initialise l'ingestion des données avec la configuration fournie."""
        self.config = config

    def download_file(self):
        """Télécharge le fichier si celui-ci n'existe pas déjà."""
        if not os.path.exists(self.config.local_data_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_url,
                filename=self.config.local_data_file
            )
            logger.info(f"{filename} téléchargé avec succès !\nInfos : \n{headers}")
        else:
            logger.info(f"Le fichier existe déjà, taille : {get_size(self.config.local_data_file)}")

    def extract_zip_file(self):
        """Décompresse le fichier ZIP téléchargé."""
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)
        logger.info(f"Extraction réussie dans {unzip_path}")
