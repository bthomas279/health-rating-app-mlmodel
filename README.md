# Machine Learning Model of the Student Health Rating App Project
**IMPORTANT NOTICE: This project is still under development.**

Planned Development
1. Model optimizations


## About 
This repository houses the machine learning model for my student mental health rating system.

## Features

## Project Structure
```
health_rating_app_mlmodel
├──health_dataset.csv               # Original dataset downloaded from Kaggle
├──nomalized_health_dataset.csv     # Normalized dataset containing relevent columns and consistent mental health scoring.
├──quant_health_dataset.csv         # health_dataset.csv but only containing relevent columns and str are now float or int.
├──reduced_health_dataset.csv       # health_dataset.csv but only containing relevent columns.
├──mental_rating_model.pkl          # Binary file of the ml model turned using joblib
├──regression_model.ipynb           # Code for the Random Forest Regressor Model
├──main.py                          # Contains FAST API to build model into API
└──scoring_norm.ipynb               # Houses the code that normalized health_dataset.csv (weights, relevent columns).



```

## Programmer
This repository is being developed by Benjamin Thomas as a part of a personal project.