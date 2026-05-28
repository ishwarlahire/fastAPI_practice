from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import pickle
import pandas as pd

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()

tier_1_cites = ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Pune", "Surat", "Jaipur"]
tier_2_cites = ["Matheran", "Lonavala", "Kasauli", "Yercaud", "Chikmagalur", "Tawang", "Ziro", "Diu", "Lachen", "Khajjiar"]

class UserInput(BaseModel):
    age: Annotated[int, Field(..., gt=0, lt=120, description="Age of the user")]
    weight: Annotated[float, Field(..., gt=0, lt=200, description="Weight of the user")]
    height: Annotated[float, Field(..., gt=0, lt=2.5, description="Height of the user")]
    income_lpa: Annotated[float, Field(..., gt=0, description="Income of the user")]
    smoker: Annotated[bool, Field(..., description="Is the user smoker")]
    city: Annotated[str, Field(..., description="City of the user")]
    occupation: Annotated[
        Literal["retired", "freelancer", "student", "government_job", "business_owner", "unemployed", "private_job"],
        Field(description="Occupation of the user")
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker and self.bmi > 27:
            return "medium"
        else:
            return "low"

    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "Adult"
        elif self.age < 60:
            return "Middle_age"
        else:
            return "Senior"

    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cites:
            return 1
        elif self.city in tier_2_cites:
            return 2
        else:
            return 3

@app.post("/predict")
def predict_premium(data: UserInput):
    input_df = pd.DataFrame([{
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200,content={"message":"predict data sucessfully","predict_category":prediction})

    # return {"prediction": prediction.tolist()}