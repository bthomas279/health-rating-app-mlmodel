#Code to create API
from fastapi import FastAPI, Form
import pickle
import numpy as np
from pydantic import BaseModel
from typing import Annotated


#Load ml model
with open("mental_rating_model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI(title="Mental Health Rating API")

class MentalData(BaseModel):
    study_hours_per_day: float
    social_media_hours: float
    netflix_hours: float
    part_time_job: int
    sleep_hours: float
    diet_quality: int
    exercise_frequency: int
    extracurricular_participation: int

#Grab user id from database
#Runs the model
@app.get("/users")
async def grab_user_data(data: Annotated[MentalData, Form()]):
    return data



