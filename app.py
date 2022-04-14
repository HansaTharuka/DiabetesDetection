# Importing essential libraries
from flask import Flask,json,render_template, request
import pickle
import numpy as np
import pandas as pd

# Load the Random Forest CLassifier model
filename = 'model2.pkl'
classifier = pickle.load(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/summary',methods=['POST'])
def summary():
    if request.method == 'POST':
        preg = int(request.form['pregnancies'])
        glucose = int(request.form['glucose'])
        bp = int(request.form['bloodpressure'])
        st = int(request.form['skinthickness'])
        insulin = int(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        age = int(request.form['age'])

        weight = float(request.form['weight'])
        height = float(request.form['height'])
        BMI = weight / (height / 100) ** 2
        if BMI <= 18.4:
            detail = 1
        elif BMI <= 24.9:
            detail = 0
        elif BMI <= 29.9:
            detail = 2
        elif BMI <= 34.9:
            detail = 2
        elif BMI <= 39.9:
            detail = 2
        else:
            detail = "You are severely obese."

        data = np.array([[preg, glucose, bp, st, insulin, BMI, dpf, age]])
        my_prediction = classifier.predict(data)
        lists = my_prediction.tolist()
        json_str = json.dumps(lists)
        print(type(json_str))

        if detail == 1 and json_str[1] == 0:
            plan = 4
        elif detail == 1 and json_str[1] == 1:
            plan = 3
        elif detail == 0:
            plan = 0
        elif detail == 2 and json_str[1] == 0:
            plan = 3
        elif detail == 2 and json_str[1] == 1:
            plan = 1


    return {
        "prediction" :json_str[1],
        "bmi": BMI,
        "plan": plan
    }

@app.route('/bmi',methods=['POST'])
def bmi():
    if request.method == 'POST':
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        BMI = weight / (height / 100) ** 2

    if BMI <= 18.4:
        detail="You are underweight."
    elif BMI <= 24.9:
        detail="You are healthy."
    elif BMI <= 29.9:
        detail="You are over weight."
    elif BMI <= 34.9:
        detail="You are severely over weight."
    elif BMI <= 39.9:
        detail="You are obese."
    else:
        detail="You are severely obese."

    return {
        "bmi" :BMI,
        "detail":detail
    }

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        preg = int(request.form['pregnancies'])
        glucose = int(request.form['glucose'])
        bp = int(request.form['bloodpressure'])
        st = int(request.form['skinthickness'])
        insulin = int(request.form['insulin'])
        bmi = float(request.form['bmi'])
        dpf = float(request.form['dpf'])
        age = int(request.form['age'])
        
        data = np.array([[preg, glucose, bp, st, insulin, bmi, dpf, age]])
        my_prediction = classifier.predict(data)

        return render_template('result.html', prediction=my_prediction)

if __name__ == '__main__':
	app.run(debug=True)