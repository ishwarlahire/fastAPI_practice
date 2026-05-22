from pydantic import BaseModel,EmailStr,AnyUrl,Field
from typing import List,Dict,Set,Optional,Annotated

class Patient(BaseModel):
    name :Annotated[
        str,
        Field(max_length=100,title='Name',
              description='Enter Name of the patient',
              examples=['Ishwar','Ram'])]
    email:EmailStr
    age:int = Field(gt=0,lt=100)
    linkedin:AnyUrl
    weight:Annotated[float,Field(gt=0,strict=True,lt=200)]
    married:Annotated[bool,Field(default=None,description='Select Your married Status')]
    allergies:Annotated[Optional[List[str]],Field(default=None, max_length=5)]
    contact_details:dict[str,str]


def insert_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("data inserted successfully")

def update_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print("data updated successfully")

patient_data={'name':"Ishwar",
              'email':'ishwarlahire2004@gmail.com',
              'age':22,
              'linkedin':'https://www.ishwarlahire.com',
              'weight':69,
              'contact_details':{'Phone':'1234567890'}}

patient1 = Patient(**patient_data)


insert_data(patient1)
update_data(patient1)
