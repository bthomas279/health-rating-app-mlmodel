#Code to create API
from fastapi import FastAPI, Form
import pickle
import uvicorn
from pydantic import BaseModel
from typing import Annotated

#Load ml model
with open("mental_rating_model.pkl", "rb") as f:
    model = pickle.load(f)

