import os
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml
import re

logger = get_logger(__name__)


def get_config(file_path):
    try:
        with open(file_path,'r') as f:
            config=yaml.safe_load(f)
            logger.info("Config read")
            return config
    except CustomException as e:
        logger.error("Error reading cofig file")
        raise CustomException("Failed to read yaml file",e)

def load_data(path):
    try:
        logger.info("Reading csv file")
        df = pd.read_csv(path)
        df = df.rename(columns = lambda x:re.sub('[^A-Za-z0-9_]+', '', x))
        logger.info("Read file")
        return df
    except CustomException as e:
        log.error("unable to read csv file")
        raise CustomeException("Error reading data",e)

