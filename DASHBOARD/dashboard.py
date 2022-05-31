import streamlit as st
import numpy as np
import pandas as pd
import requests
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

#ENV
#url_predict = 'http://mondonoke.pythonanywhere.com/predict'
#url_predict_proba0 = 'http://mondonoke.pythonanywhere.com/predictProba0'
#url_predict_proba1 = 'http://mondonoke.pythonanywhere.com/predictProba1'

#url_predict = 'http://127.0.0.1:8080/predict'
#url_predict_proba0 = 'http://127.0.0.1:8080/predictProba0'
#url_predict_proba1 = 'http://127.0.0.1:8080/predictProba1'

url_predict = 'https://bl-p7-api.herokuapp.com/predict'
url_predict_proba0 = 'https://bl-p7-api.herokuapp.com/predictProba0'
url_predict_proba1 = 'https://bl-p7-api.herokuapp.com/predictProba1'


dic_exp = pickle.load(open('./DASHBOARD/dictionnaire_explainer5.sav', 'rb'))
#dic_exp = pickle.load(open('./dictionnaire_explainerRFC5.sav', 'rb'))
df_store = pickle.load(open("./DASHBOARD/df_store_40", 'rb'))
df_model = pd.read_csv('./DASHBOARD/df_model_mini.csv')



#SIDEBAR
id_client = st.sidebar.selectbox('Client', df_model.iloc[:,0])
l_crucial_var = ["CNT_FAM_MEMBERS", "EXT_SOURCE_2", "NONLIVINGAREA_MODE",
				"EXT_SOURCE_3", "REGION_POPULATION_RELATIVE"]
st.sidebar.dataframe(df_model.loc[df_model["SK_ID_CURR"] == id_client, l_crucial_var].T)

#CENTER
st.title('Client knowledge Dashboard')

st.dataframe(df_model[df_model["SK_ID_CURR"] == id_client])
#st.dataframe(df_model[df_model["SK_ID_CURR"] == id_client].iloc[:, 2:])
data = {'id_client': id_client}




#Prediction
status = requests.post(url_predict, json=data)
val_status = status.json()

if val_status['prediction'] == "Eligible":
	statusProba = requests.post(url_predict_proba0, json=data)
	val_statusProba = statusProba.json()
elif val_status['prediction'] == "Not Eligible":
	statusProba = requests.post(url_predict_proba1, json=data)
	val_statusProba = statusProba.json()
else: 
	val_statusProba = "Error"
	

st.header(str(val_status['prediction']) + " à: "+ str(round(val_statusProba['prediction'], 2)) + "%")
#st.header(str(val_status) + " à: "+ str(round(val_statusProba, 2)) + "%")

st.components.v1.html(dic_exp[id_client], height=800)
st.header("DATAVIZ")
feature_client = st.selectbox('Variable', df_model.columns[2:])



fig = plt.figure()

a = df_store[feature_client].index
b = df_store[feature_client]

@st.cache
plt.bar(a, b, color = "black")
#plt.bar(df_store0[feature_client].index.values, df_store0[feature_client], color = "r")
#plt.bar(df_store1[feature_client].index.values, df_store1[feature_client], color = "b")
#plt.hist(df_store1[feature_client], color = "b")

#df_store = pickle.load(open("./df_store", 'rb'))
#plt.hist(df_store[feature_client], color = "r")
plt.axvline(x = df_model[df_model["SK_ID_CURR"] == id_client][feature_client].values[0], color = 'g', linestyle = '-')
#plt.axhline(y = df_mean_graph_zero[feature_client].values[0], color = 'r', linestyle = '-')
#plt.axhline(y = df_mean_graph_un[feature_client].values[0], color = 'g', linestyle = '-')
# creating subplots
#fig, ax = plt.subplots()
 
# plotting columns
#ax = sns.barplot(df_store0[feature_client], color='b')
#ax = sns.barplot(df_store1[feature_client], color='r')
 
 
st.pyplot(fig)	

