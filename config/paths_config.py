import os

########### DATA paths #######################

RAW_DIR = os.path.join("artifacts", "raw")

os.makedirs(RAW_DIR, exist_ok=True)  # This line is the crucial fix

RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")

TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")

TEST_FILE_PATH = os.path.join(RAW_DIR,"test.csv")

CONFIG_PATH = "config/config.yaml"

PROCESS_DIR = "artifacts/processed"

PROCESSED_TRAIN_PATH = os.path.join(PROCESS_DIR,"processed_train.csv")

PROCESSED_TEST_PATH = os.path.join(PROCESS_DIR,"processed_test.csv")


####### Model training Paths ########

MODEL_OUTPUT_PATH = "artifacts/models/lgbm_model.pkl"


