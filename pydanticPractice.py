from pydantic import BaseModel

class Patient(BaseModel):
    name : str
    age:int

def insert_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("data inserted successfully")

def update_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("data updated successfully")

patient_data={'name':"Ishwar",'age':22}

patient1 = Patient(**patient_data)


insert_data(patient1)
update_data(patient1)
