from flask import Flask,render_template,request,jsonify
from utils import predict_model,preprocess_text


app = Flask(__name__)
# Load the pre-trained BERT model from the saved file


# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')


# Route for handling prediction from form submission
@app.route("/predict", methods=["POST"])
def predict():
    if request.method=="POST":
         # Get the message content from the form
        message = request.form.get('content')
    # Preprocess the text
    message=preprocess_text(message)
    # Predict message using the model
    prediction = predict_model(message)
    # Map the prediction to 1 or -1
    prediction = 1 if prediction == 1 else -1
    # Render the template with the prediction and original text
    return render_template("index.html", prediction=prediction, text=message)


# API route for prediction using JSON input
@app.route('/api/predict', methods=['POST'])
def predict_api():
    data = request.get_json(force=True)  # Get data posted as a json
    # Extract the message from the JSON data
    message=data['content']
    # Preprocess the text
    message=preprocess_text(message)
    # Predict message using the model
    prediction = predict_model(message)
    # Map the prediction to 1 or -1
    prediction = 1 if prediction == 1 else -1
     # Return the prediction as JSON
    return jsonify({'prediction': prediction, 'text': message})  # Return prediction

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) 