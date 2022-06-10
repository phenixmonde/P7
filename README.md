# P7
GIT STRUCTURE

# API: https://bl-p7-api.herokuapp.com/docs
## La structure qui est déployée du côté heroku. Celle-ci contient:
### LGBMC3332_mode.sav
Le modèle LightGBMClassifier implémenté
### P7_FastAPI.py
Le script d'API
### df_model_mini.csv
Une version miniature du dataset réel sur lequel on peut faire des prédictions pour une démo

# DASHBOARD: https://share.streamlit.io/phenixmonde/p7/main/DASHBOARD/dashboard.py
## La structure qui est déployée du côté streamlit. Celle-ci contient:
### dashboard.py
Le script du dashboard streamlit
### df_model_mini.csv
Une version miniature du dataset réel sur lequel on peut faire des prédictions pour une démo
### df_store_40
La distribution des clients pour 40 features en vue de générer les graphes
### dictionnaire_explainer5.sav
Un dictionnaire contenant le lime explainer de 5 clients pour la demo

#Autres éléments importants:
### code de modelisation: https://colab.research.google.com/drive/1P5DpchoQoVNLw07zKr-fb2yBMvk_i7kb?usp=sharing
Allant du chargement de la donnée à l'implémentation du modèle
### Procfile 
utile à heroku, décrivant le déploiement
### requirements.txt
Contenant les librairies nécessaires au déploiement des scripts
### runtime.txt
Contenant la version de python nécessaire

### Se trouve dans se dossiers d'autres files:
Celle-ci pourront être amenées à être utilisées dans un futur proche afin d'améliorer les différentes parties de ce projet.
