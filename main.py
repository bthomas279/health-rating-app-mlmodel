#Code to create API
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import joblib
import uvicorn
from pydantic import BaseModel
import pandas as pd

#Load ml model
model = joblib.load("mental_rating_model.pkl")

#Define App
app = FastAPI(title="Mental Health Rating API")

#Prepare Imported data fromat (Make sure they match)
class MentalData(BaseModel):
    daily_study_hours: float
    social_media_hours: float
    tv_hours: float
    part_time_job: int
    sleep_hours: float
    diet_quality: int
    exercise_frequency_weekly: int
    extracurricular_participation: int


#Runs the model (starts on button submission)
#Important note: User Warning will appear 

@app.post("/grab/")
async def data_grab(user: MentalData):
    #Transfer data to array
    user_features = [
        user.daily_study_hours,
        user.social_media_hours,
        user.tv_hours,
        user.part_time_job,
        user.sleep_hours,
        user.diet_quality,
        user.exercise_frequency_weekly,
        user.extracurricular_participation
    ]
    
    #Change to dataframe (to match what model accepts)
    user_features_df = pd.DataFrame([user.dict()])

    #Have the model make the mental health rating
    model_prediction = model.predict(user_features_df)

    return JSONResponse({
    "rating": model_prediction[0],
    "users_data": user.dict()
    })
#Type in "fastapi dev main.py" in the console to start the application OR: 

#Click the "run python file" button
if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port=8000, reload = True)

#To access server http://127.0.0.1:8000
#To access documentation: http://127.0.0.1:8000/docs

