from utils import *
import pandas as pd
from sklearn.metrics import precision_recall_fscore_support
from bert_dataset import CustomDataset
from bert_classifier import BertClassifier
import argparse
import warnings
warnings.filterwarnings("ignore")



def test_model(path):

    """
     
    Train and Test the model 

    Parameters:
    - file_path (str): Path to the CSV or Excel file.
    -epoch (int):epoch to train the model

    Returns:
    - model object
    
    
    """

    df=read_data_file(f'DATA/{path}')
    # Drop any rows with missing values
    df = df.dropna()
    # Preprocess the text column
    df['Messages'] = df['Messages'].apply(preprocess_text)

    texts = list(df['Messages'])
    labels = list(df['gen_label'])

    predictions = [predict_model(t) for t in texts]

    precision, recall, f1score = precision_recall_fscore_support(labels, predictions,average='macro')[:3]

    print(f'precision: {precision}, recall: {recall}, f1score: {f1score}')



if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Train a model")

    # Add the required argument for the path of the training data
    parser.add_argument("test_data_file", type=str, help=" the test data")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the test_model function with the provided arguments
    test_model(args.test_data_file)