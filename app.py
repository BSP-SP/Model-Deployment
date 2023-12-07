from flask import Flask,render_template,request
from transformers import BertTokenizer
import torch

app = Flask(__name__)


tokenizer = BertTokenizer.from_pretrained('cointegrated/rubert-tiny')
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model=torch.load('Models/bert.pt')
max_len=512

def predict_model( text):
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


@app.route('/')
def home():
  
    return render_template('index.html')

@app.route("/predict", methods=["POST"])
def predict():
    if request.method=="POST":
        message = request.form.get('content')
    
    prediction = predict_model(message)
    
    prediction = 'Phishing' if prediction == 1 else 'Not Phishing'
    return render_template("index.html", prediction=prediction, text=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 