from hate.components.data_ingestion import DataIngestion
from hate.entity.config_entity import DataIngestionConfig

# DATA INGESTION TEST

if __name__ == "__main__":
    try:
        # Step 1: Create config manually (keep it simple)
        data_ingestion_config = DataIngestionConfig()

        # Step 2: Create object
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)

        # Step 3: Run ingestion
        artifacts = data_ingestion.initiate_data_ingestion()

        # Step 4: Print outputs (this is your "test")
        print("\n Data Ingestion Completed")
        print(f"Imbalance Data Path: {artifacts.imbalance_data_file_path}")
        print(f"Raw Data Path: {artifacts.raw_data_file_path}")

    except Exception as e:
        print(f"\n Error occurred: {e}")