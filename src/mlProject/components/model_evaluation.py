import os
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from urllib.parse import urlparse
import mlflow
import mlflow.sklearn
import numpy as np
import joblib
from mlProject.entity.config_entity import ModelEvaluationConfig
from mlProject.utils.common import save_json
from pathlib import Path

# Définir les variables d'environnement pour MLflow
os.environ["MLFLOW_TRACKING_URI"] = "https://dagshub.com/ngassamven/End-to-end-Machine-Learning-with-Mlflow.mlflow"
os.environ["MLFLOW_TRACKING_USERNAME"] = "ngassamven"
os.environ["MLFLOW_TRACKING_PASSWORD"] = "554295bda92465592e50bf49679ab302cd0c0392"

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self, actual, pred):
        """Calcule RMSE, MAE et R²."""
        rmse = np.sqrt(mean_squared_error(actual, pred))
        mae = mean_absolute_error(actual, pred)
        r2 = r2_score(actual, pred)
        return rmse, mae, r2

    def log_into_mlflow(self):
        """Charge le modèle, évalue les métriques et enregistre dans MLflow."""
        # Chargement des données de test
        test_data = pd.read_csv(self.config.test_data_path)
        model = joblib.load(self.config.model_path)

        # Séparation des features et de la cible
        test_x = test_data.drop(columns=[self.config.target_column])
        test_y = test_data[self.config.target_column]

        # Configuration de MLflow
        mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
        tracking_url_type_store = urlparse(mlflow.get_tracking_uri()).scheme

        with mlflow.start_run():
            # Prédictions du modèle
            predicted_values = model.predict(test_x)

            # Calcul des métriques
            rmse, mae, r2 = self.eval_metrics(test_y, predicted_values)

            # Enregistrement local des scores
            scores = {"rmse": rmse, "mae": mae, "r2": r2}
            save_json(path=Path(self.config.metric_file_name), data=scores)

            # Enregistrement des paramètres et métriques dans MLflow
            mlflow.log_params(self.config.all_params)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("r2", r2)

            # Enregistrement du modèle
            if tracking_url_type_store != "file":
                mlflow.sklearn.log_model(model, "model", registered_model_name="ElasticNetModel")
            else:
                mlflow.sklearn.log_model(model, "model")
