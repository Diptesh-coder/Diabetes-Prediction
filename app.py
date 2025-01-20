from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
import pickle

app = Flask(__name__)

# Load and prepare the dataset
def prepare_model():
    # Load the Pima Indians Diabetes Dataset
    data = pd.read_csv('https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv',
                      names=['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin',
                            'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome'])
    
    # Separate features and target
    X = data.drop('Outcome', axis=1)
    y = data['Outcome']
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    
    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    # Save the model and scaler
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

# Load the model and scaler
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)
except FileNotFoundError:
    prepare_model()
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get values from the form
        features = [float(request.form[field]) for field in [
            'pregnancies', 'glucose', 'bloodPressure', 'skinThickness',
            'insulin', 'bmi', 'diabetesPedigree', 'age'
        ]]
        
        # Scale the features
        features_scaled = scaler.transform([features])
        
        # Make prediction
        prediction = model.predict(features_scaled)
        probability = model.predict_proba(features_scaled)[0][1]
        
        # Prepare response
        result = {
            'prediction': int(prediction[0]),
            'probability': round(float(probability) * 100, 2)
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
