# Name : M Danish Zaheer
# Roll No : 25280092

# playlist followed for this part: https://www.youtube.com/watch?v=WJKsPchji0Q&list=PLKnIA16_RmvZ41tjbKB2ZnwchfniNsMuQ 

# importing necessary libraries
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib

# creating FastAPI app and loading the model
app = FastAPI() # FastAPI instance
model = joblib.load("pakwheels_svm_model.pkl")

class CarInput(BaseModel):
    # defining the inputs, if nothing is provided, it will be set to None thats what "=" is doing 
    year: int | None = None
    engine: float | None = None
    mileage: float | None = None
    city: str | None = None
    body: str | None = None
    make: str | None = None
    model: str | None = None
    transmission: str | None = None
    fuel: str | None = None
    color: str | None = None
    registered: str | None = None

# defining the home endpoint which returns a simple message to indicate that the model is running
@app.get("/")
def home():
    return {"message": "Model is running"}

# creating the predict endpoint which takes a CarInput object, processes it, and returns a prediction
@app.post("/predict")
def predict(car: CarInput):
    # converting the car input data to a dictionary and then to a dataframe while also handling missing values and creating new features
    data = car.model_dump()

    # creating new features based on the input data if the year is provided we calculate the car age otherwise we set it to nan
    if data["year"] is not None:
        data["car_age"] = 2022 - data["year"]
    else:
        data["car_age"] = np.nan

    if data["mileage"] is not None and data["year"] is not None:
        data["mileage_per_year"] = data["mileage"] / (data["car_age"] + 1)
    else:
        data["mileage_per_year"] = np.nan

    # converting the data to a dataframe and replacing None with np.nan for the model to handle missing values
    df = pd.DataFrame([data]).replace({None: np.nan})
    prediction = int(model.predict(df)[0])
    return {"prediction": prediction,
            "label": "High Price" if prediction == 1 else "Low Price"}
