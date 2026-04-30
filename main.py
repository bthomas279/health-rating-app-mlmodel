#Code to create API
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import joblib
import uvicorn
from pydantic import BaseModel
import pandas as pd
from typing import Literal

#Load ml models
reg_model = joblib.load("mental_rating_model.pkl")
class_model = joblib.load("class_mental_rating_model.pkl")

#Define App
app = FastAPI(title="Mental Health Rating API")

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
    

#Runs the model (starts on button submission)
#Important note: User Warning will appear 
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
        reg_model_prediction = reg_model.predict(user_features_df)
        class_model_prediction = None
    #Only classification
    elif request.model_type == "Classification":
        class_model_prediction = class_model.predict(user_features_df)
        reg_model_prediction = None
    #Both
    else:
        reg_model_prediction = reg_model.predict(user_features_df)
        class_model_prediction = class_model.predict(user_features_df)

    return JSONResponse({
    "reg_rating": reg_model_prediction[0] if reg_model_prediction is not None else None,
    "class_rating": class_model_prediction[0] if class_model_prediction is not None else None,
    "model_of_choice": request.model_type, 
    "users_data": request.data.dict()
    })


#Type in "fastapi dev main.py" in the console to start the application OR: 

#Click the "run python file" button
if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port=8000, reload = True)

#To access server http://127.0.0.1:8000
#To access documentation: http://127.0.0.1:8000/docs

