import os
import sys
import shutil
from hate.logger import logging
from hate.exception import CustomException
from hate.entity.config_entity import ModelPusherConfig
from hate.entity.artifact_entity import ModelPusherArtifacts

class ModelPusher:
    def __init__(self, model_pusher_config: ModelPusherConfig):
        """
        :param model_pusher_config: Configuration for model pusher
        """
        self.model_pusher_config = model_pusher_config


    
    def initiate_model_pusher(self) -> ModelPusherArtifacts:
        """
            Method Name :   initiate_model_pusher
            Description :   This method saves the trained model to the local best model directory.

            Output      :    Model pusher artifact
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")
        try:
            # Save the trained model to the local best model directory
            os.makedirs(self.model_pusher_config.BEST_MODEL_DIR, exist_ok=True)

            source_model_path = os.path.join(
                self.model_pusher_config.TRAINED_MODEL_PATH,
                self.model_pusher_config.MODEL_NAME
            )

            dest_model_path = os.path.join(
                self.model_pusher_config.BEST_MODEL_DIR,
                self.model_pusher_config.MODEL_NAME
            )

            shutil.copy2(source_model_path, dest_model_path)

            logging.info(f"Saved best model locally to {dest_model_path}")

            # Saving the model pusher artifacts
            model_pusher_artifact = ModelPusherArtifacts(
                model_path=dest_model_path
            )
            logging.info("Exited the initiate_model_pusher method of ModelPusher class")
            return model_pusher_artifact

        except Exception as e:
            raise CustomException(e, sys) from e
