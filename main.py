from fastapi import FastAPI,Path,HTTPException
import json 

app = FastAPI()

def load_data():
    with open('patients.json','r') as f:
        data = json.load(f)
    return data

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
def view_patient(patient_id:str = Path(..., description='ID from DB', example='P001')):
    #load all data
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail='Patient not found')