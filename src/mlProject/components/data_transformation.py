import os
from mlProject import logger 
from sklearn.model_selection import train_test_split
import pandas as pd
from mlProject.entity.config_entity import DataTransformationConfig



class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def train_test_spliting(self):
        """Divise les données en ensembles d'entraînement et de test."""
        data = pd.read_csv(self.config.data_path)

        # Split the data into training and test sets (75% train, 25% test)
        train, test = train_test_split(data, test_size=0.25, random_state=42)

        train.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
        test.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)

        logger.info("Données divisées en ensembles d'entraînement et de test")
        logger.info(f"Taille de l'ensemble d'entraînement : {train.shape}")
        logger.info(f"Taille de l'ensemble de test : {test.shape}")

        print(train.shape)
        print(test.shape)