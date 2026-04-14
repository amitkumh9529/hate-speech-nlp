import os
import sys
import shutil
import tensorflow.keras as keras
import pickle
import numpy as np
import pandas as pd
from hate.logger import logging
from hate.exception import CustomException
from tensorflow.keras.preprocessing.sequence import pad_sequences
from hate.constants import *
from sklearn.metrics import confusion_matrix
from hate.entity.config_entity import ModelEvaluationConfig
from hate.entity.artifact_entity import ModelEvaluationArtifacts, ModelTrainerArtifacts, DataTransformationArtifacts


class ModelEvaluation:
    def __init__(self, model_evaluation_config: ModelEvaluationConfig,
                 model_trainer_artifacts: ModelTrainerArtifacts,
                 data_transformation_artifacts: DataTransformationArtifacts):
        """
        :param model_evaluation_config: Configuration for model evaluation
        :param data_transformation_artifacts: Output reference of data transformation artifact stage
        :param model_trainer_artifacts: Output reference of model trainer artifact stage
        """

        self.model_evaluation_config = model_evaluation_config
        self.model_trainer_artifacts = model_trainer_artifacts
        self.data_transformation_artifacts = data_transformation_artifacts


    def get_best_model_from_local(self) -> str:
        """
        :return: Fetch best model from local storage directory.
                 Returns the path to the best model if it exists, otherwise returns None.
        """
        try:
            logging.info("Entered the get_best_model_from_local method of Model Evaluation class")

            os.makedirs(self.model_evaluation_config.BEST_MODEL_DIR_PATH, exist_ok=True)

            best_model_path = os.path.join(self.model_evaluation_config.BEST_MODEL_DIR_PATH,
                                           self.model_evaluation_config.MODEL_NAME)

            if os.path.isfile(best_model_path):
                logging.info(f"Best model found locally at: {best_model_path}")
                return best_model_path
            else:
                logging.info("No best model found in local storage")
                return None

        except Exception as e:
            raise CustomException(e, sys) from e


    def save_best_model_locally(self, source_model_path: str):
        """
        Save the trained model as the best model in the local best model directory.
        :param source_model_path: Path to the model to be saved as best model
        """
        try:
            logging.info("Saving the best model to local storage")

            os.makedirs(self.model_evaluation_config.BEST_MODEL_DIR_PATH, exist_ok=True)

            best_model_dest = os.path.join(self.model_evaluation_config.BEST_MODEL_DIR_PATH,
                                           self.model_evaluation_config.MODEL_NAME)

            shutil.copy2(source_model_path, best_model_dest)
            logging.info(f"Best model saved locally at: {best_model_dest}")

        except Exception as e:
            raise CustomException(e, sys) from e


    def evaluate(self, model_path=None):
        """
        :return: accuracy of the model on test data
        """
        try:
            logging.info("Entering into to the evaluate function of Model Evaluation class")
            print(self.model_trainer_artifacts.x_test_path)

            x_test = pd.read_csv(self.model_trainer_artifacts.x_test_path, index_col=0)
            print(x_test)
            y_test = pd.read_csv(self.model_trainer_artifacts.y_test_path, index_col=0)

            with open('tokenizer.pickle', 'rb') as handle:
                tokenizer = pickle.load(handle)

            model_path = model_path or self.model_trainer_artifacts.trained_model_path
            load_model = keras.models.load_model(model_path)

            x_test = x_test['tweet'].astype(str)

            # Drop any NaN or empty entries
            valid_mask = x_test.notna() & (x_test != 'nan') & (x_test != '')
            x_test = x_test[valid_mask]
            y_test = y_test[valid_mask]

            x_test = x_test.squeeze()
            y_test = y_test.squeeze()

            # Ensure all values are strings for tokenizer
            x_test = x_test.apply(str)

            test_sequences = tokenizer.texts_to_sequences(x_test)
            test_sequences_matrix = pad_sequences(test_sequences, maxlen=MAX_LEN)
            print(f"----------{test_sequences_matrix}------------------")

            print(f"-----------------{x_test.shape}--------------")
            print(f"-----------------{y_test.shape}--------------")
            import numpy as np
            evaluation = load_model.evaluate(test_sequences_matrix, np.array(y_test, dtype='float32'))
            loss, accuracy = evaluation[0], evaluation[1]
            logging.info(f"the test loss is {loss}, the test accuracy is {accuracy}")

            lstm_prediction = load_model.predict(test_sequences_matrix)
            lstm_prediction = 1 / (1 + np.exp(-lstm_prediction))
            res = []
            for prediction in lstm_prediction:
                if prediction[0] < 0.5:
                    res.append(0)
                else:
                    res.append(1)
            print(confusion_matrix(y_test, res))
            logging.info(f"the confusion_matrix is {confusion_matrix(y_test, res)} ")
            return accuracy
        except Exception as e:
            raise CustomException(e, sys) from e


    def initiate_model_evaluation(self) -> ModelEvaluationArtifacts:
        """
            Method Name :   initiate_model_evaluation
            Description :   This function is used to initiate all steps of the model evaluation

            Output      :   Returns model evaluation artifact
            On Failure  :   Write an exception log and then raise an exception
        """
        logging.info("Initiate Model Evaluation")
        try:

            logging.info("Loading currently trained model")
            trained_model = keras.models.load_model(self.model_trainer_artifacts.trained_model_path)
            with open('tokenizer.pickle', 'rb') as handle:
                load_tokenizer = pickle.load(handle)

            trained_model_accuracy = self.evaluate(self.model_trainer_artifacts.trained_model_path)

            logging.info("Fetch best model from local storage")
            best_model_path = self.get_best_model_from_local()

            logging.info("Check if best model is present in local storage or not")
            if best_model_path is None:
                is_model_accepted = True
                logging.info("No previous best model found. Currently trained model is accepted.")
                # Save the current model as the best model
                self.save_best_model_locally(self.model_trainer_artifacts.trained_model_path)

            else:
                logging.info("Load best model fetched from local storage")
                best_model = keras.models.load_model(best_model_path)
                best_model_accuracy = self.evaluate(best_model_path)

                logging.info("Comparing accuracy between best_model and trained_model")
                if trained_model_accuracy > best_model_accuracy:
                    is_model_accepted = True
                    logging.info("Trained model is better. Accepted and saving as new best model.")
                    # Replace the best model with the new trained model
                    self.save_best_model_locally(self.model_trainer_artifacts.trained_model_path)
                else:
                    is_model_accepted = False
                    logging.info("Trained model is not better. Keeping previous best model.")

            model_evaluation_artifacts = ModelEvaluationArtifacts(is_model_accepted=is_model_accepted)
            logging.info("Returning the ModelEvaluationArtifacts")
            return model_evaluation_artifacts

        except Exception as e:
            raise CustomException(e, sys) from e
