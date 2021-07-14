from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Present_Price=float(request.form['Present_Price'])
        Kms_Driven=int(request.form['Kms_Driven'])
        Kms_Driven2=np.log(Kms_Driven)
        Owner=int(request.form['Owner'])
        Fuel_Type=request.form['Fuel_Type']

        if(Fuel_Type=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Diesel=0
        elif(Fuel_Type=='Diesel'):
            Fuel_Type_Petrol=0
            Fuel_Type_Diesel=1
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 0

        Year=2021-Year

        Seller_Type_Individual = request.form['Seller_Type_Individual']

        if(Seller_Type_Individual=='Individual'):
            Seller_Type_Individual=1
        else:
            Seller_Type_Individual=0

        Transmission_Mannual=request.form['Transmission_Mannual']
        if(Transmission_Mannual=='Mannual'):
            Transmission_Mannual=1
        else:
            Transmission_Mannual=0

        model = pickle.load(open('xgboost.pkl', 'rb'))
        standard_scaler = pickle.load(open('standard_scaler.pkl', 'rb'))

        prediction = model.predict(standard_scaler.transform([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel,Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]]))
        output = prediction[0]

        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text=f'You Can Sell The Car at Rs {round(100000*output)}')
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(port=5002,debug=True)

