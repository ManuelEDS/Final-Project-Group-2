# Overview
The project aims to predict the probability of hospitalization for elderly Mexican individuals using machine learning algorithms and data such as demographics, health indicators, and medical history. The model can help healthcare providers identify high-risk patients and allocate resources accordingly. This project is similar to what you have implemented in the last few sprints but with a focus on building a model that can use a few features to make accurate predictions.

# Deliverables
Goal: The main goal of this project is to ask users to complete a form and use the provided information to predict the risk of hospitalization for that person in the next year. For that task, a Machine Learning model must be trained to make that prediction. Keep in mind the dataset we are going to use has thousands of features but, we can't ask users to complete such amount of fields in the form. We suggest you start using some classic models like Decision Trees, Random Forests, or Gradient Boosting, identify the most important features, and try to refine your model input based on that.

In order to graduate from the ML Developer Career, you have to approve the Main Deliverables. You are also welcome to complete the Optional Deliverables if you want to continue to add experience and build your portfolio, although those are not mandatory.

Main Deliverables:

* Exploratory Dataset Analysis (EDA)
* Scripts used for data pre-processing and data preparation
* Training scripts and trained models. Description of how to reproduce results
* Implementation and training of model for hospitalization prediction
* The final model should need less than 50 features to make predictions
* The final model AUC Score must be over 0.9
* Present results and a demo of the model doing predictions in real time using an API
* Make an UI in which users must complete a form to get the prediction for the demo
* Everything must be containerized using Docker


# Using GitHub

* git config --global user.name "Tu Nombre"
* git config --global user.email "tu@email.com"

* git clone https://github.com/ManuelEDS/Final-Project-Group-2

* git branch -r # Lista los branches remotos
* git push -u origin main # Genera el origin/main en el remoto

Para hacer commit de los cambios:
1) Cargar el SOURCE CONTROL con los comentarios del cambio
2) Commit
3) Pull

Cuando parto del repositorio, desde el directorio inicial...
git init
git remote add origin https://github.com/ManuelEDS/Final-Project-Group-2/
git remote -v # Para verificar la conexión al repo remoto
git pull origin main # Combina git fetch y git merge

## ----------------------------------------

To test the streamlit
python -m venv env
.\env\scripts\activate 
pip install -r ./requirements.txt

.\env\scripts\activate 
streamlit run ui/hospital_classifier_app.py


## ----------------------------------------
# Docker


## Instalación

/
docker network prune # Eliminé network anteriores
docker network create shared_network
docker-compose up --build -d

/api # No debiera estar nada abajo porque necesita "db"
docker-compose up # Esto me mostro la generación de la base de datos!

/
docker-compose up


## Database
psql -U postgres -d sp3
\l : lista las bases de datos
\dt : lista las tablas
\c <database-name> : swith to db



