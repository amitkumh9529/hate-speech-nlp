import os
import sys
from zipfile import ZipFile
from hate.logger import logging
from hate.exception import CustomException
import shutil
from hate.entity.config_entity import DataIngestionConfig
from hate.entity.artifact_entity import DataIngestionArtifacts


class DataIngestion:
    def __init__(self, data_ingestion_config : DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
        


    def get_data_from_local(self) -> None:
        try:
            logging.info("Entered the get_data_from_local method of Data ingestion class")

            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok=True)

            # Compute path relative to project root so it works cross-platform
            # (Windows locally and Linux on Streamlit Cloud)
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            source_path = os.path.join(project_root, "data", "dataset.zip")
            destination_path = self.data_ingestion_config.ZIP_FILE_PATH

        # Copy file from local path to artifacts directory
        
            shutil.copy(source_path, destination_path)

            logging.info(f"Copied dataset from {source_path} to {destination_path}")
            logging.info("Exited the get_data_from_local method of Data ingestion class")

        except Exception as e:
            raise CustomException(e, sys) from e
        
    def unzip_and_clean(self):
        try:
            logging.info("Entered unzip_and_clean")

            with ZipFile(self.data_ingestion_config.ZIP_FILE_PATH, 'r') as zip_ref:
                zip_ref.extractall(self.data_ingestion_config.ZIP_FILE_DIR)
            logging.info("Exited the unzip_and_clean method of Data ingestion class")
            return (
                self.data_ingestion_config.DATA_ARTIFACTS_DIR,
                self.data_ingestion_config.NEW_DATA_ARTIFACTS_DIR
            )

        except Exception as e:
            raise CustomException(e, sys) from e
            
            
    

    def initiate_data_ingestion(self) -> DataIngestionArtifacts:
        logging.info("Entered the initiate_data_ingestion method of Data ingestion class")

        try:
            self.get_data_from_local()
            logging.info("Fetched the data from local directory")
            imbalance_data_file_path, raw_data_file_path = self.unzip_and_clean()
            logging.info("Unzipped file and split into train and valid")

            data_ingestion_artifacts = DataIngestionArtifacts(
                imbalance_data_file_path= imbalance_data_file_path,
                raw_data_file_path = raw_data_file_path
            )

            logging.info("Exited the initiate_data_ingestion method of Data ingestion class")

            logging.info(f"Data ingestion artifact: {data_ingestion_artifacts}")

            return data_ingestion_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e