import os
import io
import sys
import re
import tensorflow.keras as keras
import pickle
import numpy as np
from PIL import Image
from hate.logger import logging
from hate.constants import *
from hate.exception import CustomException
from tensorflow.keras.preprocessing.sequence import pad_sequences
from hate.components.data_transforamation import DataTransformation
from hate.entity.config_entity import DataTransformationConfig
from hate.entity.artifact_entity import DataIngestionArtifacts


class PredictionPipeline:
    def __init__(self):
        self.model_name = MODEL_NAME
        self.model_path = os.path.join("artifacts", "PredictModel")
        self.data_transformation = DataTransformation(data_transformation_config= DataTransformationConfig,data_ingestion_artifacts=DataIngestionArtifacts)
        self._model = None
        self._tokenizer = None
        self._loaded_model_path = None
        self._loaded_model_mtime = None

    def _contains_direct_abuse(self, text: str) -> bool:
        normalized_text = re.sub(r"[^a-z\s]", " ", str(text).lower())
        normalized_text = re.sub(r"\s+", " ", normalized_text).strip()
        direct_abuse_patterns = [
            r"\bfuck\s+you\b",
            r"\bfuck\s+off\b",
            r"\bgo\s+fuck\s+yourself\b",
            r"\byou\s+are\s+(a\s+)?bitch\b",
            r"\byou(?:re|'re)?\s+(a\s+)?bitch\b",
        ]
        return any(re.search(pattern, normalized_text) for pattern in direct_abuse_patterns)



    
    def get_model_from_local(self) -> str:
        """
        Method Name :   get_model_from_local
        Description :   This method loads the best model from local storage
        Output      :   best_model_path
        """
        logging.info("Entered the get_model_from_local method of PredictionPipeline class")
        try:
            import shutil
            # Loading the best model from local storage
            os.makedirs(self.model_path, exist_ok=True)
            best_model_path = os.path.join(self.model_path, self.model_name)

            # Always check for a newer model and update PredictModel
            artifacts_base = os.path.join(os.getcwd(), "artifacts")
            latest_model = None

            # 1. Check artifacts/best_model/ (saved by model_pusher)
            best_model_candidate = os.path.join(artifacts_base, "best_model", self.model_name)
            if os.path.exists(best_model_candidate):
                latest_model = best_model_candidate

            # 2. Fall back to latest timestamped artifacts directory
            if latest_model is None and os.path.exists(artifacts_base):
                for dir_name in sorted(os.listdir(artifacts_base), reverse=True):
                    candidate = os.path.join(artifacts_base, dir_name, "ModelTrainerArtifacts", self.model_name)
                    if os.path.exists(candidate):
                        latest_model = candidate
                        break

            # Copy the latest model to PredictModel if it's newer or doesn't exist
            if latest_model:
                should_copy = not os.path.exists(best_model_path)
                if not should_copy:
                    # Copy if source is newer than current PredictModel
                    should_copy = os.path.getmtime(latest_model) > os.path.getmtime(best_model_path)
                if should_copy:
                    shutil.copy2(latest_model, best_model_path)
                    logging.info(f"Updated PredictModel from {latest_model}")

            if not os.path.exists(best_model_path):
                raise FileNotFoundError(
                    "No trained model found. Please train the model first."
                )

            logging.info("Exited the get_model_from_local method of PredictionPipeline class")
            return best_model_path

        except Exception as e:
            raise CustomException(e, sys) from e

    def load_artifacts(self, model_path):
        """Load the trained model and tokenizer once, then reuse them."""
        try:
            model_mtime = os.path.getmtime(model_path)
            should_reload = (
                self._model is None
                or self._tokenizer is None
                or self._loaded_model_path != model_path
                or self._loaded_model_mtime != model_mtime
            )

            if should_reload:
                self._model = keras.models.load_model(model_path)
                with open("tokenizer.pickle", "rb") as handle:
                    self._tokenizer = pickle.load(handle)
                self._loaded_model_path = model_path
                self._loaded_model_mtime = model_mtime

            return self._model, self._tokenizer

        except Exception as e:
            raise CustomException(e, sys) from e

    
    def predict(self,best_model_path,text):
        """Predict whether input text is hate speech or not"""
        logging.info("Running the predict function")
        try:
            import tensorflow as tf
            load_model, load_tokenizer = self.load_artifacts(best_model_path)

            if self._contains_direct_abuse(text):
                print("hate and abusive")
                return "hate and abusive"
            
            text=self.data_transformation.concat_data_cleaning(text)
            text = [text]            
            print(text)
            seq = load_tokenizer.texts_to_sequences(text)
            padded = pad_sequences(seq, maxlen=300)
            print(seq)
            raw_pred = load_model.predict(padded)
            # Apply sigmoid since model outputs raw logits (from_logits=True)
            pred = tf.sigmoid(raw_pred).numpy()
            score = float(np.squeeze(pred))
            print("pred", pred)
            if score > 0.5:

                print("hate and abusive")
                return "hate and abusive"
            else:
                print("no hate")
                return "no hate"
        except Exception as e:
            raise CustomException(e, sys) from e

    
    def run_pipeline(self,text):
        logging.info("Entered the run_pipeline method of PredictionPipeline class")
        try:

            best_model_path: str = self.get_model_from_local() 
            predicted_text = self.predict(best_model_path,text)
            logging.info("Exited the run_pipeline method of PredictionPipeline class")
            return predicted_text
        except Exception as e:
            raise CustomException(e, sys) from e
