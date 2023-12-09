from utils import preprocess_text,read_data_file
from transformers import BertTokenizer
import torch
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from bert_dataset import CustomDataset
from bert_classifier import BertClassifier
import argparse
import warnings
warnings.filterwarnings("ignore")



def train_model(path,epochs=5):

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
    # Split the dataset into training and testing sets
    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

    # Load the pre-trained BERT tokenizer 
    tokenizer_path='bert-base-uncased'
    tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
    # Check if a GPU is available, otherwise use the CPU
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # Set the maximum length for tokenized sequences
    max_len=512
    
    classifier = BertClassifier(
        model_path=tokenizer_path,
        tokenizer_path=tokenizer_path,
        n_classes=2,
        epochs=epochs,
        model_save_path='Models/bert.pt'
                                            )
    classifier.preparation(
        X_train=list(train_data['Messages']),
        y_train=list(train_data['gen_label']),
        X_valid=list(test_data['Messages']),
        y_valid=list(test_data['gen_label'])
    )
    classifier.train()

    texts = list(test_data['Messages'])
    labels = list(test_data['gen_label'])

    predictions = [classifier.predict(t) for t in texts]

    precision, recall, f1score = precision_recall_fscore_support(labels, predictions,average='macro')[:3]

    print('-----------Test Data Metrics------------------')
    print(f'precision: {precision}, recall: {recall}, f1score: {f1score}')
    return classifier

if __name__=='__main__':
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Train a model")

    # Add the required argument for the path of the training data
    parser.add_argument("train_data_file", type=str, help=" training data")

    # Add an optional argument for the number of epochs (default is 10)
    parser.add_argument("--epochs", type=int, default=5, help="Number of epochs (default is 5)")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the train_model function with the provided arguments
    train_model(args.train_data_file, args.epochs)