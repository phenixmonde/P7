from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from pyngrok import ngrok
import nest_asyncio
import uvicorn
import pickle
import pandas as pd
from pydantic import BaseModel
import lightgbm
import typing as T
import numpy as np
from pydantic import BaseModel
from markupsafe import escape

filename = './API/LGBMC332_model.sav'
model = pickle.load(open(filename, 'rb'))

df_model = pd.read_csv('./API/df_model_mini.csv')

preds_proba = model.predict_proba(df_model.iloc[:,2:])

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
	
	print(df_model[df_model["SK_ID_CURR"] == id_client_received].iloc[:,0:])
	
	print(df_model[df_model["SK_ID_CURR"] == id_client_received].iloc[:,0:].shape)
	
	print(type(df_model[df_model["SK_ID_CURR"] == id_client_received].iloc[:,2:].squeeze()))
	
	print(type(df_model[df_model["SK_ID_CURR"] == id_client_received].iloc[:,2:].squeeze().array))
	
	df_check = df_model[df_model["SK_ID_CURR"] == id_client_received].iloc[:,2:]
	
	#prediction = model.predict(df_model[df_model["SK_ID_CURR"] == id_client_received].iloc[:,2:])
	prediction = model.predict(df_check)
	if(prediction[0]==1):
		prediction= "Not Eligible"
	else:
		prediction= "Eligible"
		
	print(type(prediction))
	
	return {'prediction': prediction}

@app.post('/predictProba0')
def predictProba0(data: Client):
	data = data.dict()
	id_client_received = data['id_client']
	
	index_predsProba = df_model[df_model["SK_ID_CURR"]==id_client_received].index.values[0]
	print(index_predsProba)
	
	return {'prediction': preds_proba[index_predsProba][0]}
	#return {'prediction': model.predict_proba(df_model.iloc[index_predsProba,2:])[0]}
	
@app.post('/predictProba1')
def predictProba1(data: Client):
	data = data.dict()
	id_client_received = data['id_client']
	
	index_predsProba = df_model[df_model["SK_ID_CURR"]==id_client_received].index.values[0]
	print(index_predsProba)
	
	return {'prediction': preds_proba[index_predsProba][1]}
	#return {'prediction': model.predict_proba(df_model.iloc[index_predsProba,2:])[1]}

#if __name__ == '__main__':
#    app.run()
	
#nest_asyncio.apply()
#uvicorn.run(app, host='127.0.0.1', port=8080)
