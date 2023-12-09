
from transformers import BertTokenizer
import torch
import pandas as pd
import re



def read_data_file(file_path):
    """
    Read data from either CSV or Excel file.

    Parameters:
    - file_path (str): Path to the CSV or Excel file.

    Returns:
    - pd.DataFrame: A pandas DataFrame containing the data.
    """
    try:
        # Attempt to read as CSV
        data = pd.read_csv(file_path)
        return data
    except pd.errors.ParserError:
        try:
            # Attempt to read as Excel
            data = pd.read_excel(file_path)
            return data
        except pd.errors.ParserError:
            # If neither CSV nor Excel format is successful, raise an error
            raise ValueError(f"Unable to read data from the file: {file_path}")


def preprocess_text(text):

    """
    clean the data

    Parameters:
    - text (str): 

    Returns:
    - pd.DataFrame: A pandas DataFrame containing the data.
    """
    # Clean the text by removing special characters, URLs, etc.
    emoj=re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    text=re.sub(emoj, '', text)
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove non-alphabetic characters
    text = text.lower()  # Convert to lowercase
    return text


def predict_model( text):
        
        tokenizer = BertTokenizer.from_pretrained('cointegrated/rubert-tiny')
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        model=torch.load('Models/bert.pt')
        max_len=512
        encoding = tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=max_len,
            return_token_type_ids=False,
            truncation=True,
            padding='max_length',
            return_attention_mask=True,
            return_tensors='pt',
        )
        
        out = {
              'text': text,
              'input_ids': encoding['input_ids'].flatten(),
              'attention_mask': encoding['attention_mask'].flatten()
          }
        
        input_ids = out["input_ids"].to(device)
        attention_mask = out["attention_mask"].to(device)
        
        outputs = model(
            input_ids=input_ids.unsqueeze(0),
            attention_mask=attention_mask.unsqueeze(0)
        )
        
        prediction = torch.argmax(outputs.logits, dim=1).cpu().numpy()[0]

        return prediction
