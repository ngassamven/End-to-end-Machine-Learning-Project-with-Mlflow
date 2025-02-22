from mlProject.constants import *
from mlProject.utils.common import read_yaml,create_directories
from mlProject.entity.config_entity import ( DataIngestionConfig, 
                                            DataValidationConfig,
                                            DataTransformationConfig,
                                            ModelTrainerConfig,
                                            ModelEvaluationConfig)
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
    



    def get_data_transformation_config(self) -> DataTransformationConfig:
        """Récupère la configuration pour la transformation des données."""
        config = self.config["data_transformation"]  # Dictionnaire contenant la config de transformation

        # Créer les répertoires nécessaires
        create_directories([Path(config["root_dir"])])

        # Retourner l'objet DataTransformationConfig
        return DataTransformationConfig(
            root_dir=Path(config["root_dir"]),
            data_path=Path(config["data_path"])  # Correction ici
        )

    def get_model_trainer_config(self) -> ModelTrainerConfig:
        """Récupère la configuration pour l'ingestion des données."""
        config  = self.config["model_trainer"]
        params = self.params["ElasticNet"]
        schema = self.schema["TARGET_COLUMN"]


        # Créer les répertoires nécessaires
        create_directories([Path(config["root_dir"])])

        
        # Retourner l'objet DataTransformationConfig
        return ModelTrainerConfig(
            root_dir=Path(config["root_dir"]),
            train_data_path= Path(config["train_data_path"]),
            test_data_path= Path(config["test_data_path"]),
            model_name= config["model_name"],  # Pas besoin de Path pour une string simple
            alpha= params["alpha"],  # ⬅️ Garde ça comme float
            l1_ratio= params["l1_ratio"],  # ⬅️ Garde ça comme float
            target_column = schema["name"]
)
    


    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        try:
            config = self.config["model_evaluation"]
        except KeyError:
            raise KeyError("Missing 'model_evaluation' section in the configuration file.")
    
        params = self.params["ElasticNet"]
        schema = self.schema["TARGET_COLUMN"]

    # Create the necessary directories
        create_directories([Path(config["root_dir"])])

    # Return the ModelEvaluationConfig object
        return ModelEvaluationConfig(
            root_dir=Path(config["root_dir"]),
            test_data_path=Path(config["test_data_path"]),
            model_path=config["model_path"],
            all_params=params,
            metric_file_name=Path(config["metric_file_name"]),
            target_column=schema["name"],
            mlflow_uri="https://dagshub.com/ngassamven/End-to-end-Machine-Learning-with-Mlflow.mlflow",
    )