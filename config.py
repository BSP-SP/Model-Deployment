from transformers import BertTokenizer
import torch
 # Load the pre-trained BERT tokenizer for the Russian language
tokenizer_path='bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
# Check if a GPU is available, otherwise use the CPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Set the maximum length for tokenized sequences
max_len=512