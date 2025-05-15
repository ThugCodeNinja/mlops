import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import get_config,load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self,train_path,test_path,processed_dir,config_path):

        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = get_config(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def process_data(self,df):
        try:
            logger.info("Attempting to perform data processing")
            logger.info("Dropping unwanted columns")
            df.drop(columns=["Booking_ID"],inplace = True)
            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_columns"]
            num_cols = self.config["data_processing"]["numerical_columns"]

            label_encoder = LabelEncoder()

            mappings = {}
            logger.info("Label encoding categorical columns")
            for i in cat_cols:
                df[i] = label_encoder.fit_transform(df[i])
                mappings[i] = {label:code for label,code in zip(label_encoder.classes_,label_encoder.transform(label_encoder.classes_))}

            logger.info(f"mappings are: {mappings}")

            logger.info("Data skewness check")

            skewness_threshold = self.config["data_processing"]["skewness_threshold"]

            skew_measure = df[num_cols].apply(lambda x: x.skew())
            

            for col in num_cols:
                if skew_measure[col] > skewness_threshold:
                    df[col] = np.log1p(df[col])

            return df

        except CustomException as e:
            logger.error(f"error in processing data {e}")
            raise CustomeException ("Error processing data",e)
    
    def balance_data(self,df):
        try:
            logger.info("balancing data")
            x = df.drop(columns="booking_status")
            y = df["booking_status"]
            smote = SMOTE(random_state=42)

            x_res,y_res = smote.fit_resample(x,y)
            balanced_df = pd.DataFrame(x_res, columns = x.columns)
            balanced_df["booking_status"] = y_res
            logger.info(f"New shape{balanced_df.shape}. Balanced successfully")

            return balanced_df
        except CustomException as e:
            logger.error(f"Error in balancing stage {e}")
            raise CustomException ("Error in balancing class samples",e)

    def select_features(self,df):
        try:
            model = RandomForestClassifier(random_state = 42)
            x = df.drop(columns="booking_status")
            y = df["booking_status"]
            model.fit(x,y)
            feature_importance = model.feature_importances_
            fi_df = pd.DataFrame({
                "Features": x.columns,
                "Importance": feature_importance
            })
            fi_df.sort_values(by = "Importance",ascending=False)
            num_features = self.config["data_processing"]["number_of_features"]
            top_10_features = fi_df["Features"].head(num_features).values
            top_10_df = df[top_10_features.tolist()+["booking_status"]]

            logger.info("feature selection done")

            return top_10_df

        except CustomException as e:
            logger.error(f"Error is feature selection code")
            raise CustomException("Error in feature selection",e)

    def save_data(self,df,file_path):
        try:
            logger.info("Saving processed data to file")
            df.to_csv(file_path,index=False)
            logger.info("done")
        except CustomeException as e:
            raise CustomException('Error saving file to path',e)


    def process(self):
        try:
            logger.info("Loading RAW data")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            train_df = self.process_data(train_df)
            test_df = self.process_data(test_df)

            train_df = self.balance_data(train_df)
            test_df = self.balance_data(test_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df,PROCESSED_TRAIN_PATH)
            self.save_data(test_df,PROCESSED_TEST_PATH)
        except CustomException as e:
            logger.error(f"Error in balancing stage {e}")
            raise CustomException ("Error in balancing class samples",e)


if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH,TEST_FILE_PATH,PROCESS_DIR,CONFIG_PATH)
    print("object made")
    processor.process()
        

        
