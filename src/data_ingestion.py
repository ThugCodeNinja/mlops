from src.logger import get_logger
from src.custom_exception import CustomException
import pandas as pd
from sklearn.model_selection import train_test_split 
from google.cloud import storage 
import os
from config.paths_config import *
from utils.common_functions import get_config

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.bucket_file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR,exist_ok=True)

        logger.info(f"Data ingestion started for {self.bucket_name} consisting of this file - {self.bucket_file_name}")


    def download_csv_file(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.bucket_file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"Downloading file to path {RAW_FILE_PATH}")
        except CustomException as e:
            logger.error(f"Error downloading to path {RAW_FILE_PATH}")
            raise CustomException("Error donwloading file",e)
        

    def split(self):
        try:
            logger.info(f"Splitting data as per ratio {self.train_ratio}")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data,test_data = train_test_split(data,test_size=1-self.train_ratio, random_state = 42)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
        except CustomException as e:
            logger.error(f"Error splitting {RAW_FILE_PATH}")
            raise CustomException("Error splitting file",e)
        
    def run(self):
        try:
            logger.info("Starting execution")
            self.download_csv_file()
            self.split()
            logger.info("Done")

        except CustomException as e:
            logger.error("Execution failed",str(e))

        finally:
            logger.error("ingestion_process done")

if __name__=="__main__":
    obj = DataIngestion(get_config(CONFIG_PATH))
    obj.run()
