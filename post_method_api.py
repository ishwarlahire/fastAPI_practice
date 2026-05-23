from fastapi import FastAPI,HTTPException,Path,Query
from pydantic import BaseModel,Field,computed_field
from typing import Dict ,AnyStr,Annotated,Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='Enter Patient id',examples=["P001"])]
    name:Annotated[str,Field(...,description='Enter Patient Name' , examples="Ishwar Lahire")]
    city:Annotated[str,Field(...,description="Enter Patient city name",examples='Pune')]
    age:Annotated[int,Field(...,description="Enter patient Currunt Age",gt=0,lt=150,examples=59)]
    gender:Annotated[Literal['Male','Female','Other'],Field(description='select Patient Gender male,Female,Other',examples="Male")]
    height:Annotated[float,Field(description="Enter Patient Height in meter",examples=3.1,gt=0,lt=5)]
    weight:Annotated[float,Field(description="Enter Patient Weight in KG", examples=56.78,gt=0,lt=150)]

    @computed_field
    @property
    def BMI(self) ->float:
        BMI = self.weight/self.height**2
        return BMI
    @computed_field
    @property
    def verdict(self) ->str:
        if self.BMI < 18.5:
            return "Under Weight"
        elif self.BMI>18.5 and self.BMI<30:
            return "Normal"
        else:
            return "Obese"
        
    @classmethod
    def load_data():
        with open("patient.json","r") as f:
            data = json.load(f)
        return data

@app.get("/")
def hello():
    return {"message":"hello! How are you?"}

@app.get("/about")
def about():
    return {"message":"This page created with FastAPI and Pydantic library"}

@app.post("/create")
def createPatient():
    pass