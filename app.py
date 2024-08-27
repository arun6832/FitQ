from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# Load the trained model
with open('model.pkl', 'rb') as model_file:
    dtree = pickle.load(model_file)

# Load the label encoders
with open('label_encoder.pkl', 'rb') as encoders_file:
    encoders = pickle.load(encoders_file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        smoking_habit = request.form['smoking_habit']
        alcohol_consumption = request.form['alcohol_consumption']
        screen_time_hours = request.form['screen_time_hours']
        sleep_duration_hours = request.form['sleep_duration_hours']
        water_intake_liters = float(request.form['water_intake_liters'])

        # Convert inputs to numerical using the loaded LabelEncoders
        smoking_habit_encoded = encoders['smoking_habit'].transform([smoking_habit])[0]
        alcohol_consumption_encoded = encoders['alcohol_consumption'].transform([alcohol_consumption])[0]
        screen_time_hours_encoded = encoders['screen_time_hours'].transform([screen_time_hours])[0]
        sleep_duration_hours_encoded = encoders['sleep_duration_hours'].transform([sleep_duration_hours])[0]

        # Create input array for the model
        input_features = np.array([[smoking_habit_encoded, alcohol_consumption_encoded, screen_time_hours_encoded, sleep_duration_hours_encoded, water_intake_liters]])

        # Predict using the loaded model
        prediction = dtree.predict(input_features)

        return render_template('index.html', prediction=prediction[0])

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
