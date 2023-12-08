from flask import Flask,render_template,request,jsonify
from utils import predict_model,preprocess_text
app = Flask(__name__)



@app.route('/')
def home():
    return render_template('index.html')



@app.route("/predict", methods=["POST"])
def predict():
    if request.method=="POST":
        message = request.form.get('content')
    message=preprocess_text(message)
    prediction = predict_model(message)
    prediction = 1 if prediction == 1 else -1
    
    return render_template("index.html", prediction=prediction, text=message)



@app.route('/api/predict', methods=['POST'])
def predict_api():
    data = request.get_json(force=True)  # Get data posted as a json
    message=data['content']
    message=preprocess_text(message)
    prediction = predict_model(message)
    prediction = 1 if prediction == 1 else -1
    
    return jsonify({'prediction': prediction, 'text': message})  # Return prediction

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 