import streamlit as st
import numpy as np
import pandas as pd
import requests
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

#ENV
#url = 'http://127.0.0.1:8080/predict'
url_predict = 'http://127.0.0.1:5000/predict'
url_predict_proba0 = 'http://127.0.0.1:5000/predictProba0'
url_predict_proba1 = 'http://127.0.0.1:5000/predictProba1'

filename = './dictionnaire_explainer5.sav'



#df_mean_graph_un = pd.read_csv("./1/df_mean_graph.csv", index_col=0).T
#df_mean_graph_zero = pd.read_csv("./0/df_mean_graph0.csv", index_col=0).T
df_raw_graph = pd.read_csv("./raw_mini.csv")

dic_exp = pickle.load(open(filename, 'rb'))
df_store = pickle.load(open("./df_store", 'rb'))
#df_store0 = pickle.load(open("./0/df_store0", 'rb'))
#df_store1 = pickle.load(open("./1/df_store1", 'rb'))


df_model = pd.read_csv('./df_model_mini.csv')
df_raw_mini = pd.read_csv('./raw_mini.csv')

#SIDEBAR
id_client = st.sidebar.selectbox('Client', df_model.iloc[:,0])
data = {'id_client': id_client}
l_crucial_var = ["CNT_FAM_MEMBERS", "EXT_SOURCE_2", "NONLIVINGAREA_MODE",
				"EXT_SOURCE_3", "REGION_POPULATION_RELATIVE"]
st.sidebar.dataframe(df_raw_mini.loc[df_raw_mini["SK_ID_CURR"] == id_client, l_crucial_var].T)
#st.sidebar.dataframe(df_raw_mini.loc[df_raw_mini["SK_ID_CURR"] == id_client, df_raw_mini.columns.values[3:]].T)

#CENTER
st.title('Client knowledge Dashboard')

#Prediction
status = requests.post(url_predict, params=data)
val_status = status.json()
if status == "Eligible":
	statusProba = requests.post(url_predict_proba1, params=data)
else:
	statusProba = requests.post(url_predict_proba0, params=data)
#x = requests.post(url, json=data)

val_statusProba = statusProba.json()

#st.write("Status= " + str(y['prediction']))

st.header(str(val_status) + " à: "+ str(round(val_statusProba, 2)) + "%")

#with st.sidebar:
#	st.components.v1.html(dic_exp[id_client], height=800)
#feature_client = st.selectbox('info client', df_model.columns[2:])

st.components.v1.html(dic_exp[id_client], height=800)
st.header("DATAVIZ")
feature_client = st.selectbox('Variable', df_model.columns[2:])

#for i in df_model.columns[2:]:
#	if str(feature_client) == str(i)[0:len(feature_client)]:
#		k = str(i)

#df_column_desc = pd.read_csv("./HomeCredit_columns_description.csv")
#st.write(df_column_desc[df_column_desc["ROW"]==k][i])

fig = plt.figure()


plt.bar(df_store[feature_client].index.values, df_store[feature_client], color = "black")
#plt.bar(df_store0[feature_client].index.values, df_store0[feature_client], color = "r")
#plt.bar(df_store1[feature_client].index.values, df_store1[feature_client], color = "b")
#plt.hist(df_store1[feature_client], color = "b")

#df_store = pickle.load(open("./df_store", 'rb'))
#plt.hist(df_store[feature_client], color = "r")
plt.axvline(x = df_raw_graph[df_raw_graph["SK_ID_CURR"] == id_client][feature_client].values[0], color = 'g', linestyle = '-')
#plt.axhline(y = df_mean_graph_zero[feature_client].values[0], color = 'r', linestyle = '-')
#plt.axhline(y = df_mean_graph_un[feature_client].values[0], color = 'g', linestyle = '-')
# creating subplots
#fig, ax = plt.subplots()
 
# plotting columns
#ax = sns.barplot(df_store0[feature_client], color='b')
#ax = sns.barplot(df_store1[feature_client], color='r')
 
# renaming the axes
#ax.set(xlabel="x-axis", ylabel="y-axis")
 
st.pyplot(fig)	

# a gauche: titre - id client - classification
# a droite: graphes comparatif avec moyenne des variables impactantes lime
