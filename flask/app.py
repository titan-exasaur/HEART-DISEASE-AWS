from flask import *
import os,sys
app = Flask(__name__)

user_id = 'admin'
user_pwd = 'admin123'

@app.route('/')
def log():
    return render_template('login.html')

@app.route('/submit_log',methods=['GET','POST'])
def log_sub():
    if request.method=='POST':
        uid = request.form['uid']
        upwd = request.form['pwd']
        error = 'Invalid Credentials'

        if uid == user_id and upwd == user_pwd:
            return render_template('index.html')
        else:
            return render_template('login.html',error=error)

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/eda')
def eda():
    return render_template('eda.html')

@app.route('/detector')
def detector():
    return render_template('detector.html')

@app.route('/model_parameter')
def model_parameter():
    return render_template('model_parameter.html')

# @app.route('/display/<filename>')
# def display_image(filename):
#     # print('display_image filename: ' + filename)
#     return redirect(url_for('static_new', filename='uploads/' + filename))

@app.route('/submit_detector', methods=['POST'])
def choose_file():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    import joblib

    import warnings
    warnings.filterwarnings('ignore')

    model = joblib.load('/media/kumar/HDD1/INFIDATA/EXPERIMENT LAB/3 [KNSIT] HEART DISEASE/flask/stacked_model.pkl')

# Create an empty dictionary to store user inputs
    user_inputs = {}
    if request.method == 'POST':
        age = int( request.form['age'])
        sex = int(request.form['sex'])
        chest_pain_type = int( request.form['chest_pain_type'])
        resting_blood_pressure = int(request.form['resting_blood_pressure'])
        cholesterol = int(request.form['cholesterol'])
        fasting_blood_sugar = int(request.form['fasting_blood_sugar'])
        resting_ecg = int(request.form['resting_ecg'])
        max_heart_rate = int(request.form['max_heart_rate'])
        exercise_induced_angina = int(request.form['exercise_induced_angina'])
        st_depression = float(request.form['st_depression'])
        slope = int(request.form['slope'])
        major_vessels_number = int(request.form['major_vessels_number'])
        thal = int(request.form['thal'])

        new_user_input = [[age, sex, chest_pain_type,
                   resting_blood_pressure, cholesterol,
                   fasting_blood_sugar, resting_ecg, max_heart_rate,
                   exercise_induced_angina, st_depression, slope,
                   major_vessels_number, thal]]
        # print(new_user_input)
        scaler = joblib.load('/media/kumar/HDD1/INFIDATA/EXPERIMENT LAB/3 [KNSIT] HEART DISEASE/flask/scaler.pkl')

        new_user_input_scaled = scaler.transform(new_user_input)

        new_user_output = model.predict(new_user_input_scaled)[0]
        if new_user_output == 0:
            op = "No Heart Disease"
        if new_user_output == 1:
            op = "Risk of Heart Disease Found"
        # print(new_user_output)
        return render_template('detector.html',output=op)



if __name__=='__main__':
    app.run(host="0.0.0.0",port=80,debug=True)