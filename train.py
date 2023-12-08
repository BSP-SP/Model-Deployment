from utils import preprocess_text
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_recall_fscore_support
from bert_dataset import CustomDataset
from bert_classifier import BertClassifier
import argparse
import warnings
warnings.filterwarnings("ignore")



def train_model(path,epochs=5):

    df=pd.read_csv(path)
    # Drop any rows with missing values
    df = df.dropna()
    # Preprocess the text column
    df['Messages'] = df['Messages'].apply(preprocess_text)
    # Split the dataset into training and testing sets
    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)

    
    classifier = BertClassifier(
        model_path='cointegrated/rubert-tiny',
        tokenizer_path='cointegrated/rubert-tiny',
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
    parser.add_argument("train_data_path", type=str, help="Path to the training data")

    # Add an optional argument for the number of epochs (default is 10)
    parser.add_argument("--epochs", type=int, default=5, help="Number of epochs (default is 5)")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the train_model function with the provided arguments
    train_model(args.train_data_path, args.epochs)