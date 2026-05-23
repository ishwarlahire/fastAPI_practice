from fastapi import FastAPI,HTTPException,Path,Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Dict ,AnyStr,Annotated,Literal
import json

app = FastAPI()

class Patient(BaseModel):
    id:Annotated[str,Field(...,description='Enter Patient id',examples=["P001"])]
    name:Annotated[str,Field(...,description='Enter Patient Name' , examples=["Ishwar Lahire"])]
    city:Annotated[str,Field(...,description="Enter Patient city name",examples=['Pune'])]
    age:Annotated[int,Field(...,description="Enter patient Currunt Age",gt=0,lt=150,examples=[59])]
    gender:Annotated[Literal['Male','Female','Other'],Field(description='select Patient Gender male,Female,Other',examples=["Male"])]
    height:Annotated[float,Field(description="Enter Patient Height in meter",examples=[3.1],gt=0,lt=5)]
    weight:Annotated[float,Field(description="Enter Patient Weight in KG", examples=[56.78],gt=0,lt=150)]

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
        
    
def load_data():
    with open("patients.json","r") as f:
        data = json.load(f)
    return data
def save_data(data):
    with open("patients.json",'w') as f:
        json.dump(data,f)



@app.get("/")
def  hello():
    return {"message":"hello from fastAPI This is a first app"}

@app.get("/about")
def about():
    return{"message":"This is a fast API application"}

@app.get('/view')
def view():
    data = load_data()
    return data

@app.get('/patient/{patient_id}')  #using Path Parameter
def view_patient(patient_id:str = Path(..., description='ID from DB', examples=['P001'])):
    #load all data
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient not found')

@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description='sort on the basis of hight ans weight or BMI'),order:str = Query('asc',description='sort in asc or desc orders')):
    valid_fields = ['height','weight','BMI']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail= f'Invalid field select from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail=f'Invalid order selection between asc and desc')
    data = load_data()
    sort_order = True if order=='desc' else False
    sorted_data = sorted(data.values(),key = lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data

#post APIs
@app.post("/create")
def createPatient(patient:Patient):
    #load data in database
    data = load_data()
    #ceck data in database
    if patient.id in data:
        raise HTTPException(status_code=409,detail="Patient olready exist in database.")
    #create new patient
    data[patient.id] = patient.model_dump(exclude={"id"})
    #save patient data in database
    save_data(data)
    #return message
    return JSONResponse(status_code=201,content={"message":"Patient create successfully"})
