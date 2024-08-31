import pandas as pd
from flask import Flask, request, render_template
import pickle
import os 

app = Flask(__name__)


model = pickle.load(open("model.sav", "rb"))

@app.route("/")
def loadPage():
    return render_template('index.html', query="")

@app.route("/", methods=['POST'])
def predict():
    
    input_data = [
        request.form['query1'], request.form['query2'], request.form['query3'], request.form['query4'],
        request.form['query5'], request.form['query6'], request.form['query7'], request.form['query8'],
        request.form['query9'], request.form['query10'], request.form['query11'], request.form['query12'],
        request.form['query13'], request.form['query14'], request.form['query15'], request.form['query16'],
        request.form['query17'], request.form['query18'], request.form['query19']
    ]
    
    
    input_data[0] = 1 if input_data[0] == "Yes" else 0
    
   
    input_df = pd.DataFrame([input_data], columns=[
        'SeniorCitizen', 'MonthlyCharges', 'TotalCharges', 'gender', 
        'Partner', 'Dependents', 'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
        'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
        'PaymentMethod', 'tenure'
    ])
    

  
    input_df['tenure_group'] = pd.cut(input_df['tenure'].astype(int), range(1, 80, 12), right=False, labels=[
        "1 - 12", "13 - 24", "25 - 36", "37 - 48", "49 - 60", "61 - 72"
    ])
    
    
    input_df.drop(columns=['tenure'], inplace=True)
    
   
    encoded_input = pd.get_dummies(input_df, columns=[
        'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
        'MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup',
        'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies',
        'Contract', 'PaperlessBilling', 'PaymentMethod', 'tenure_group'
    ])
    
   
    model_columns = pickle.load(open("model_columns.pkl", "rb"))
    encoded_input = encoded_input.reindex(columns=model_columns, fill_value=0)
    
    
    prediction = model.predict(encoded_input)
    probability = model.predict_proba(encoded_input)[:, 1]
    
    
    
   
    if prediction[0] == 1:
        output1 = "This customer is likely to churn."
        output2 = "Confidence: {:.2f}%".format(probability[0] * 100)
    elif prediction[0] == 0:
        output1 = "This customer is likely to stay."
        output2 = "Confidence: {:.2f}%".format(probability[0] * 100)
        
    
    return render_template('index.html', output1=output1, output2=output2, 
                           query1=request.form['query1'], 
                           query2=request.form['query2'],
                           query3=request.form['query3'],
                           query4=request.form['query4'],
                           query5=request.form['query5'], 
                           query6=request.form['query6'], 
                           query7=request.form['query7'], 
                           query8=request.form['query8'], 
                           query9=request.form['query9'], 
                           query10=request.form['query10'], 
                           query11=request.form['query11'], 
                           query12=request.form['query12'], 
                           query13=request.form['query13'], 
                           query14=request.form['query14'], 
                           query15=request.form['query15'], 
                           query16=request.form['query16'], 
                           query17=request.form['query17'],
                           query18=request.form['query18'], 
                           query19=request.form['query19'])

if __name__ == '__main__':
    app.run(debug=True, port=8000)



