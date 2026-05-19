#Code to create API
#Imports
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import joblib
import uvicorn
from pydantic import BaseModel
import pandas as pd
from typing import Literal, Optional, List
from datetime import datetime
from dotenv import load_dotenv
import os

#Import chart functions
from visuals import (numerical_plot, categorical_plot, sleep_hours_plot, study_hours_plot)


#Define port
load_dotenv()
port = os.getenv("PORT")

#Load ml models
reg_model = joblib.load("mental_rating_model.pkl")
class_model = joblib.load("class_mental_rating_model.pkl")


#Define App
app = FastAPI(title="Mental Health Rating API")

#Data Import Structures-------------------
#Prepare Imported data fromat for Regression (Make sure they match)
class MentalData(BaseModel):
    daily_study_hours: float
    social_media_hours: float
    tv_hours: float
    part_time_job: int
    sleep_hours: float
    diet_quality: int
    exercise_frequency_weekly: int
    extracurricular_participation: int

#Request format for the type of model to be used 
#Separates the model_type and the data to be read
class PredictionRequest(BaseModel):
    model_type: Literal["Classification", "Regression", "Both"]
    data: MentalData


#Request format for the columns the user wants to be plotted
class RowSelections(BaseModel):
    #Rating columns
    regression_ratings: Optional[float] = None
    classification_ratings: Optional[str] = None

    #Habit columns
    study_hours: Optional[float] = None
    sleep_hours: Optional[float] = None

    #Created_at cloumn
    time: datetime

#Class for current user request
class PlotRequest(BaseModel):
    user_request: Literal["sleep", "study", "regRate", "classRate"]
    data: List[RowSelections]

#Define valid types of strings and charts
VALID_TYPES = {
    "numerical_mental_health": numerical_plot,
    "categorical_mental_health": categorical_plot,
    "sleep_hours": sleep_hours_plot,
    "study_hours": study_hours_plot,
}

#REQUESTS/RESPONSES------------------------------------
#Runs the model (starts on button submission)
@app.post("/predict/")
async def data_grab(request: PredictionRequest):
    
    #Change to dataframe (to match what model accepts)
    user_features_df = pd.DataFrame([request.data.dict()])

    #Test the stuff gathered
    print(user_features_df)
    print(request.model_type)

    #Have the model make the mental health rating based on type
    #Only Regression
    if request.model_type == "Regression":
        reg_model_prediction = reg_model.predict(user_features_df)*10
        class_model_prediction = None
    #Only classification
    elif request.model_type == "Classification":
        class_model_prediction = class_model.predict(user_features_df)
        reg_model_prediction = None
    #Both
    else:
        reg_model_prediction = reg_model.predict(user_features_df)*10
        class_model_prediction = class_model.predict(user_features_df)

    if reg_model_prediction is not None:
        reg_model_prediction = [round(value, 2) for value in reg_model_prediction]
    return JSONResponse({
    "reg_rating": reg_model_prediction[0] if reg_model_prediction is not None else None,
    "class_rating": class_model_prediction[0] if class_model_prediction is not None else None,
    "model_of_choice": request.model_type, 
    "users_data": request.data.dict()
    })

@app.post("/plot/")
async def plot_development(request: PlotRequest):
    try:
        choice = request.user_request
        data = request.data
        if choice == "regRate":
            image_b64 = numerical_plot(data)
        if choice == "classRate":
            image_b64 = categorical_plot(data)
        if choice == "sleep":
            image_b64 = sleep_hours_plot(data)
        if choice == "study":
            image_b64 = study_hours_plot(data)
    
        return {"image": image_b64, "type": choice}
    
    #Find errors in plots
    except Exception as e:
        return {"error": type(e).__name__, "detail": str(e)}



#Type in "fastapi dev main.py" in the console to start the application OR: 

#Click the "run python file" button
if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port=8000, reload = True)


