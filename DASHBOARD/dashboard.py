import streamlit as st
import numpy as np
import pandas as pd
import requests
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

#ENV
url_predict = 'http://Mondonoke.pythonanywhere.com/predict'
url_predict_proba0 = 'http://Mondonoke.pythonanywhere.com/predictProba0'
url_predict_proba1 = 'http://Mondonoke.pythonanywhere.com/predictProba1'

dic_exp = pickle.load(open('./DASHBOARD/dictionnaire_explainer5.sav', 'rb'))
df_store = pickle.load(open("./DASHBOARD/df_store_40", 'rb'))
df_model = pd.read_csv('./DASHBOARD/df_model_mini.csv')

#SIDEBAR
id_client = st.sidebar.selectbox('Client', df_model.iloc[:,0])
data = {'id_client': id_client}
l_crucial_var = ["CNT_FAM_MEMBERS", "EXT_SOURCE_2", "NONLIVINGAREA_MODE",
				"EXT_SOURCE_3", "REGION_POPULATION_RELATIVE"]
st.sidebar.dataframe(df_model.loc[df_model["SK_ID_CURR"] == id_client, l_crucial_var].T)

#CENTER
st.title('Client knowledge Dashboard')

#Prediction
status = requests.post(url_predict, params=data)
val_status = status.json()
if status == "Eligible":
	statusProba = requests.post(url_predict_proba1, params=data)
else:
	statusProba = requests.post(url_predict_proba0, params=data)

val_statusProba = statusProba.json()

st.header(str(val_status) + " à: "+ str(round(val_statusProba, 2)) + "%")


st.components.v1.html(dic_exp[id_client], height=800)
st.header("DATAVIZ")
feature_client = st.selectbox('Variable', df_model.columns[2:])


fig = plt.figure()


plt.bar(df_store[feature_client].index.values, df_store[feature_client], color = "black")
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

