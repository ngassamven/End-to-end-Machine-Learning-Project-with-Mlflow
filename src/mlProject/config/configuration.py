from mlProject.constants import *
from mlProject.utils.common import read_yaml,create_directories
from mlProject.entity.config_entity import ( DataIngestionConfig, 
                                            DataValidationConfig)
from pathlib import Path

# Définir les chemins par défaut
CONFIG_FILE_PATH = "config/config.yaml"
PARAMS_FILE_PATH = "params.yaml"
SCHEMA_FILE_PATH = "schema.yaml"

class ConfigurationManager:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH, schema_filepath=SCHEMA_FILE_PATH):
        """Charge les fichiers YAML de configuration et crée les répertoires nécessaires."""
        self.config = read_yaml(Path(config_filepath))
        self.params = read_yaml(Path(params_filepath))
        self.schema = read_yaml(Path(schema_filepath))

        # Créer le répertoire racine des artifacts
        create_directories([self.config["artifacts_root"]])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        """Récupère la configuration pour l'ingestion des données."""
        config = self.config["data_ingestion"]  # Dictionnaire contenant la config d'ingestion

        # Créer les répertoires nécessaires
        create_directories([Path(config["root_dir"])])

        # Retourner l'objet DataIngestionConfig
        return DataIngestionConfig(
            root_dir=Path(config["root_dir"]),
            source_url=config["source_URL"],  # Assurez-vous que la clé est bien "source_URL" dans config.yaml
            local_data_file=Path(config["local_data_file"]),
            unzip_dir=Path(config["unzip_dir"])
        )
    


    def get_data_validation_config(self) -> DataValidationConfig:
        """Récupère la configuration pour l'ingestion des données."""
        config = self.config["data_validation"]  # Dictionnaire contenant la config d'ingestion
        schema = self.schema["COLUMNS"]


        # Créer les répertoires nécessaires
        create_directories([Path(config["root_dir"])])

        # Retourner l'objet DataIngestionConfig
        return DataValidationConfig (
            root_dir=Path(config["root_dir"]),
            STATUS_FILE=config["STATUS_FILE"],  
            unzip_data_dir=Path(config["unzip_data_dir"]),  # Correction de la parenthèse
            all_schema=schema   # Correction : utilisation du dictionnaire
        )
