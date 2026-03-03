#Code to create API
from fastapi import FastAPI, Form
import pickle
import uvicorn
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


#Runs the model
#Run uvicorn main:app --reload in terminal to start
#To access server http://127.0.0.1:8000
#To access documentation: http://127.0.0.1:8000/docs
@app.post("/users/")
async def grab_user_data(data: Annotated[MentalData, Form()]):
    return data
#Type in "fastapi dev main.py" in the console to start the application OR: 

#Click the "run python file" button
if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port=8000, reload = True)


