import pandas as pd
import joblib
import os
import lightgbm as lgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.model_params import *
from config.paths_config import *
from utils.common_functions import get_config,load_data
from scipy.stats import randint
import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTrainer:
    def __init__(self,train_path,test_path,model_output_path):
        self.train_path = train_path
        self.test_path  = test_path
        self.config = get_config(CONFIG_PATH)
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGM_PARAMETERS
        self.random_dist = RANDOM_SEARCH_PARAMETERS

    def load_and_split(self):
        try:
            logger.info(f"Reading file {self.train_path}")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info("Data split successfully")

            return X_train,y_train,X_test,y_test
        
        except CustomException as e:
            logger.error("Unable to split data")
            raise CustomException("Unable to split",e)


    def train_lgbm(self,X_train,y_train):

        try:
            logger.info("Initializing model training")
            model = lgb.LGBMClassifier(random_state = self.random_dist['random_state'])

            logger.info("Staring hypertuning of parameters")

            random_search = RandomizedSearchCV(
                estimator = model,
                param_distributions = self.params_dist,
                n_iter = self.random_dist["n_iter"],
                cv = self.random_dist["cv"],
                random_state = self.random_dist["random_state"],
                verbose = self.random_dist["verbose"],
                n_jobs = self.random_dist["n_jobs"],
                scoring = self.random_dist["scoring"]
            )

            logger.info("Training model")

            random_search.fit(X_train,y_train)

            logger.info("Done")

            best_params = random_search.best_params_

            best_lgbm_model = random_search.best_estimator_

            logger.info(f"best params are {best_params}")

            return best_lgbm_model

        except CustomException as e:
            logger.error("Training failed")
            raise CustomException ("Taining failes",e)



    def evaluate_model(self,X_test,y_test,model):
        try:
            logger.info("Evaluating trained model")

            y_pred = model.predict(X_test)

            accuracy = accuracy_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred) 
            recall = recall_score(y_test,y_pred) 
            f1 = f1_score(y_test,y_pred)

            logger.info(f'accuracy: {accuracy}')
            logger.info(f'precision: {precision}')
            logger.info(f'recall: {recall}')
            logger.info(f'f1-score {f1}')

            return {
                'accuracy' : accuracy,
                'precision' : precision,
                'recall' : recall,
                "f1" : f1
            }

        except CustomException as e:
            logger.error("Evaluation failed")
            raise CustomException ("Evaluation failed",e)


    def save_model(self,model):

        try:
            os.makedirs(os.path.dirname(self.model_output_path),exist_ok = True)

            joblib.dump(model,self.model_output_path)

            logger.info("saved model successfully")
        except CustomException as e:
            logger.error("Error in saving model")
            raise CustomException("Error in saving model",e)

    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Splitting data")

                logger.info("Starting MLFLOW experimentation tracking")

                mlflow.log_artifact(self.train_path, artifact_path = 'datasets')

                mlflow.log_artifact(self.test_path, artifact_path = 'datasets')

                X_train,y_train,X_test,y_test = self.load_and_split()

                logger.info("Training model")
                model = self.train_lgbm(X_train,y_train)
                logger.info("Evaluating model")
                result = self.evaluate_model(X_test,y_test,model)
                logger.info(f"The model evalution metrics are: {result}")
                logger.info("Saving model")
                self.save_model(model)
                logger.info("Logging the model to mlflow")
                mlflow.log_artifact(self.model_output_path)
                mlflow.log_params(model.get_params())
                mlflow.log_metrics(result)
        except CustomException as e:
            logger.error("Error in training model")
            raise CustomException("Error in training model",e)


if __name__ =="__main__":
    model_trainer = ModelTrainer(PROCESSED_TRAIN_PATH,PROCESSED_TEST_PATH,MODEL_OUTPUT_PATH)
    model_trainer.run()