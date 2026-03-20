#Code to create API
from fastapi import FastAPI, Form
import joblib
import uvicorn
from pydantic import BaseModel
from typing import Annotated


#Load ml model
model = joblib.load("mental_rating_model.pkl")

app = FastAPI(title="Mental Health Rating API")

class MentalData(BaseModel):
    daily_study_hours: float
    social_media_hours: float
    tv_hours: float
    part_time_job: int
    sleep_hours: float
    diet_quality: int
    exercise_frequency_weekly: int
    extracurricular_participation: int

#Runs the model
#Run uvicorn main:app --reload in terminal to start
#To access server http://127.0.0.1:8000
#To access documentation: http://127.0.0.1:8000/docs

@app.post("/grab/")
async def data_grab(user: MentalData):
    print(user)
    print(user.dict())
    return {"FastAPI got the data!"}
#Type in "fastapi dev main.py" in the console to start the application OR: 

#Click the "run python file" button
if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port=8000, reload = True)


