from src.data_ingestion import DataIngestion
from src.data_preprocessing import DataProcessor
from src.model_training import ModelTrainer
from utils.common_functions import *
from config.paths_config import *

if __name__ == "__main__":
    #Data ingestion
    data_ingestion = DataIngestion(get_config(CONFIG_PATH))
    data_ingestion.run()
    #Data preprocessing
    processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESS_DIR,CONFIG_PATH)
    processor.process()
    #Model training
    model_trainer = ModelTrainer(PROCESSED_TRAIN_PATH,PROCESSED_TEST_PATH,MODEL_OUTPUT_PATH)
    model_trainer.run()
    
