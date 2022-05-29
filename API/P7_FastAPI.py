#from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddleware
#from fastapi.middleware.wsgi import WSGIMiddleware
from pyngrok import ngrok
import nest_asyncio
import uvicorn
import pickle
import pandas as pd
from pydantic import BaseModel
#from sklearn.model_selection import train_test_split
#from sklearn.ensemble import RandomForestClassifier
import lightgbm
import typing as T
import numpy as np
from pydantic import BaseModel
#import flask
#from flask import request, jsonify
from markupsafe import escape
# import streamlit as st

#filename = './LGBMC332_model.sav'
filename = './RFC_model200.sav'
model = pickle.load(open(filename, 'rb'))

df_model = pd.read_csv('./df_model_mini.csv')
#X = df_model.iloc[:,2:]
#y = df_model.iloc[:,1]
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

#preds = model.predict(X_test.iloc[0:2,:])
#preds = model.predict(df_model.iloc[0:2,2:])

#preds_proba = model.predict_proba(df_model.iloc[:,2:])

class Client(BaseModel):
    id_client: int

app = FastAPI()

@app.get('/')
def index():
    return {'message': 'Hello, World'}

@app.get('/{name}')
def get_name(name: str):
    return {'Welcome To Dashboard': f'{name}'}


@app.post('/predict')
def predict(data: Client):
	data = data.dict()
	id_client_received = data['id_client']
	#id_client_received = data
	print(id_client_received)
	df_check = df_model[df_model["SK_ID_CURR"] == id_client_received].iloc[:,2:].squeeze().array.reshape(1, -1)
	#prediction = model.predict(df_model[df_model["SK_ID_CURR"] == id_client_received].iloc[:,2:])
	prediction = model.predict(df_check)
	if(prediction[0]==1):
		prediction= "Not Eligible"
	else:
		prediction= "Eligible"
		
	print(type(prediction))
	
	return {'prediction': prediction}

#app = flask.Flask(__name__)

#app.route('/')
#def hello():
 #   return 'Hello, World!'

#@app.route("/predict", methods=['POST'])
#def predict():
	#id_client = id_client.dict()
	#id_client_received = id_client['id_client']
#	id_client_received = int(request.args.get('id_client'))
	#id_client_received = id_client_received.get('id_client_received')
	#id_client_received = escape(id_client)
	
#	prediction = model.predict(df_model[df_model["SK_ID_CURR"] == id_client_received].iloc[:,2:])
	
#	if(prediction[0] == 1):
#		prediction = "Not Eligible"
#	else:
#		prediction = "Eligible"
		
	#return(prediction)
#	return jsonify(prediction)
	
#@app.route("/predictProba0", methods=['POST'])
#def predictProba0():
#	id_client_received = int(request.args.get('id_client'))
	
#	index_predsProba = df_model[df_model["SK_ID_CURR"]==id_client_received].index.values[0]
#	return jsonify(preds_proba[index_predsProba][0])
	
#@app.route("/predictProba1", methods=['POST'])
#def predictProba1():
#	id_client_received = int(request.args.get('id_client'))
	
#	index_predsProba = df_model[df_model["SK_ID_CURR"]==id_client_received].index.values[0]
#	return jsonify(preds_proba[index_predsProba][1])

#if __name__ == '__main__':
#    app.run()
	
#nest_asyncio.apply()
#uvicorn.run(app, host='127.0.0.1', port=8080)
