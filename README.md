# Machine Learning Model of the Student Health Rating App Project

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## About 
This repository houses the machine learning model for my student mental health rating system.
This aspect of the project has two goals: to create machine learning models to predict the mental health of students, and to create user-tailored visualizations of specific data. Both of these features are then sent back to the main server to be viewed by the user.

## Features
- Grabs user data information collected by Node.js to have the ML models predict current mental health.
- Grabs user data information collected by Node.js to create Matplotlib visualizations.
- Extraction and responses are performed by a serverless FastAPI server.

## Project Structure
```
datasets/
├──health_dataset.csv               # Original dataset downloaded from Kaggle
├──nomalized_health_dataset.csv     # Normalized dataset containing relevent columns and consistent mental health scoring.
├──quant_health_dataset.csv         # health_dataset.csv but only containing relevent columns and str are now float or int.
└──reduced_health_dataset.csv       # health_dataset.csv but only containing relevent columns.

model_operations/
├──classification_model.ipynb       # Code for the Random Forest Classifier Model
├──regression_model.ipynb           # Code for the Random Forest Regressor Model
└──scoring_norm.ipynb               # Houses the code that normalized health_dataset.csv (weights, relevent columns).

visual_operations/
└──visuals.py                       #Code to develop/design user visuals, and prepare them for response sending

├──mental_rating_model.pkl          # Binary file of the regression ml model turned using joblib
├──class_mental_rating_model.pkl    # Binary file of the classification ml model turned using joblib
├──main.py                          # Contains FAST API to build model into API and run responses (also main file for vercel deployment)
├──vercel.json                      # Source for vercel deployment
└──requirements.txt                 # Library requirements for deployment

```

## Programmer
This repository was developed by Benjamin Thomas as a part of a personal project.
