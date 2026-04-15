# Hate Speech Classification

An end-to-end NLP project that classifies user-entered text as either **hate/offensive content** or **no hate**. The project includes data ingestion, text preprocessing, model training, model evaluation, model persistence, a prediction pipeline, and a Streamlit web application for interactive use.

Live App: https://hate-speech-nlp-whhzywbaq8uugmfkc94hqs.streamlit.app

## Problem Statement

Online platforms receive large volumes of user-generated text every day. Manually reviewing this content is slow, inconsistent, and difficult to scale. Harmful, abusive, or offensive language can negatively affect user safety and community quality if it is not detected quickly.

The goal of this project is to build a machine learning system that can automatically analyze text and predict whether it belongs to one of two classes:

```text
1 = hate/offensive
0 = no hate
```

## Solution

This project solves the problem using a binary NLP classification pipeline. Raw tweet data is cleaned, labels are normalized into a binary format, text is tokenized and padded, and an LSTM-based deep learning model is trained to classify the text.

The final application is deployed with Streamlit, allowing users to:

- Enter text and receive a prediction.
- Train the model from the UI.
- View whether the content is classified as safe or hate/offensive.

The prediction pipeline loads the trained model and saved tokenizer, applies the same preprocessing used during training, converts the text into padded sequences, and returns the final classification.

## Key Features

- End-to-end machine learning pipeline structure.
- Binary hate/offensive text classification.
- Tweet text preprocessing and normalization.
- Keras tokenizer and sequence padding.
- LSTM-based neural network model.
- Model evaluation and best-model saving.
- Streamlit web interface.
- Docker support for containerized deployment.
- Streamlit Cloud deployment support.

## Tech Stack

| Category | Tools |
| --- | --- |
| Language | Python |
| Data Processing | Pandas, NumPy |
| NLP | NLTK, Keras Tokenizer |
| Machine Learning | TensorFlow, Keras, Scikit-learn |
| Model Architecture | Embedding, SpatialDropout1D, LSTM, Dense |
| Visualization | Matplotlib, Seaborn |
| Web App | Streamlit |
| Packaging | setup.py |
| Deployment | Streamlit Community Cloud, Docker |

## Dataset

The project uses tweet-based hate speech datasets. One dataset contains three original classes:

```text
0 = hate speech
1 = offensive language
2 = neither
```

For this project, the task is converted into binary classification:

```text
0 hate speech        -> 1 hate/offensive
1 offensive language -> 1 hate/offensive
2 neither            -> 0 no hate
```

The project processes more than **56,000 text samples** after combining the available datasets.

## Model Performance

During experimentation, the LSTM model achieved approximately:

```text
Validation Accuracy: 93.56%
Test Accuracy:       92.85%
```

Note: These metrics came from the experimental training run. After any preprocessing, label-mapping, or pipeline changes, the model should be retrained and the metrics should be regenerated.

## ML Pipeline

The project follows a modular pipeline design.

```text
Data Ingestion
      |
      v
Data Transformation
      |
      v
Model Training
      |
      v
Model Evaluation
      |
      v
Model Pusher
      |
      v
Prediction Pipeline
      |
      v
Streamlit UI
```

### 1. Data Ingestion

Responsible for reading the dataset from local storage, extracting the dataset zip file, and saving raw data files into the artifacts directory.

Main file:

```text
hate/components/data_ingestion.py
```

### 2. Data Transformation

Responsible for cleaning and preparing the dataset for training.

Main tasks:

- Drop unnecessary columns.
- Convert multiclass labels into binary labels.
- Combine datasets.
- Convert text to lowercase.
- Remove URLs, punctuation, HTML tags, newline characters, and words containing numbers.
- Apply stemming.
- Drop empty or missing text rows.
- Save the final transformed CSV file.

Main file:

```text
hate/components/data_transforamation.py
```

### 3. Model Training

Responsible for training the LSTM model.

Main tasks:

- Read transformed data.
- Validate labels.
- Drop missing text values.
- Split data into train and test sets.
- Tokenize text using Keras Tokenizer.
- Pad sequences to a fixed length.
- Train the LSTM model.
- Save the trained model.
- Save the tokenizer.

Main file:

```text
hate/components/model_trainer.py
```

### 4. Model Evaluation

Responsible for evaluating the trained model on test data.

Main tasks:

- Load trained model.
- Load tokenizer.
- Transform test data into padded sequences.
- Evaluate loss and accuracy.
- Generate predictions.
- Create a confusion matrix.
- Compare trained model with the existing best model.

Main file:

```text
hate/components/model_evaluation.py
```

### 5. Model Pusher

Responsible for saving the accepted trained model into the local best-model directory.

Main file:

```text
hate/components/model_pusher.py
```

### 6. Prediction Pipeline

Responsible for making predictions on user input.

Main tasks:

- Load the latest trained model.
- Load the saved tokenizer.
- Clean input text.
- Convert text to sequence.
- Apply padding.
- Generate model score.
- Apply sigmoid to logits.
- Return final class label.

Main file:

```text
hate/pipeline/prediction_pipeline.py
```

## Model Architecture

The model is an LSTM-based binary classifier:

```text
Embedding Layer
SpatialDropout1D
LSTM
Dense Output Layer
```

The model outputs raw logits and is trained using:

```python
BinaryCrossentropy(from_logits=True)
```

During prediction, sigmoid is applied to convert the raw logit into a probability. A probability greater than `0.5` is classified as hate/offensive.

## Project Structure

```text
.
├── app.py
├── ui.py
├── requirements.txt
├── setup.py
├── Dockerfile
├── .dockerignore
├── tokenizer.pickle
├── data/
│   └── dataset.zip
├── hate/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_transforamation.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluation.py
│   │   └── model_pusher.py
│   ├── pipeline/
│   │   ├── train_pipeline.py
│   │   └── prediction_pipeline.py
│   ├── ml/
│   │   └── model.py
│   ├── entity/
│   │   ├── config_entity.py
│   │   └── artifact_entity.py
│   ├── constants/
│   ├── logger/
│   └── exception/
└── artifacts/
```

## How to Run Locally

Clone the repository:

```bash
git clone <your-repository-url>
cd <your-project-folder>
```

Create and activate a virtual environment:

```bash
conda create -n hate python=3.10 -y
conda activate hate
```

Install dependencies:

```bash
pip install -r requirements.txt
pip install -e .
```

Run the Streamlit app:

```bash
streamlit run ui.py
```

Or run through `app.py`:

```bash
python app.py
```

Then open:

```text
http://localhost:8080
```

## Run Training

Training can be started from the Streamlit UI, or directly from the command line:

```bash
python -c "from hate.pipeline.train_pipeline import TrainPipeline; TrainPipeline().run_pipeline()"
```

After training, the model is saved as:

```text
model.h5
```

The tokenizer is saved as:

```text
tokenizer.pickle
```

## Run Prediction From Command Line

```bash
python -c "from hate.pipeline.prediction_pipeline import PredictionPipeline; print(PredictionPipeline().run_pipeline('fuck you'))"
```

Example output:

```text
hate and abusive
```

## Docker Usage

Build the Docker image:

```bash
docker build -t hate-speech-app .
```

Run the container:

```bash
docker run -p 8080:8080 hate-speech-app
```

Open:

```text
http://localhost:8080
```

## Streamlit Deployment

This project can be deployed for free using Streamlit Community Cloud.

Basic deployment steps:

1. Push the project to GitHub.
2. Go to Streamlit Community Cloud.
3. Connect your GitHub repository.
4. Select the branch.
5. Set the main file path as:

```text
ui.py
```

6. Deploy the app.

## Important Notes

- The same tokenizer used during training must be used during prediction.
- The same text preprocessing logic should be used in both training and prediction.
- Since the model outputs logits, sigmoid must be applied before thresholding predictions.
- Binary classification requires labels to be only `0` and `1`.
- Accuracy alone is not enough for hate speech detection; precision, recall, F1-score, and confusion matrix are useful additional metrics.

## Future Improvements

- Add precision, recall, F1-score, ROC-AUC, and PR-AUC reporting.
- Improve preprocessing for emojis, hashtags, mentions, slang, and repeated characters.
- Add experiment tracking with MLflow.
- Add dataset and model versioning.
- Fine-tune a transformer model such as BERT or DistilBERT.
- Add automated tests for preprocessing, label mapping, and prediction.
- Deploy as an API using FastAPI.

## Author

Amit
