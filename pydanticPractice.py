from typing import Annotated, List, Optional
from pydantic import (
    AnyUrl,
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
    computed_field,
)
class Address(BaseModel):
    city:str
    taluka:str
    state:str
    pincode:int

class Patient(BaseModel):
    # Patient Name
    name: Annotated[
        str,
        Field(
            max_length=100,
            title="Name",
            description="Enter name of the patient",
            examples=["Ishwar", "Ram"],
        ),
    ]    
    email: EmailStr # Email Validation
    age: int = Field(gt=0, lt=100) #Age Validation
    linkedin: AnyUrl  # LinkedIn URL
    weight: Annotated[
        float,
        Field(gt=0, lt=200, strict=True),
    ] # Weight Validation
    height:Annotated[
        float,
        Field(gt=0,lt=200,strict=True)]

    married: Annotated[
        Optional[bool],
        Field(
            default=None,
            description="Select your married status",
        ),
    ]   # Married Status

    allergies: Annotated[
        Optional[List[str]],
        Field(default=None, max_length=5),
    ]# Allergies List

    contact_details: dict[str, str]   # Contact Details
    address:Address

    # ---------------- FIELD VALIDATORS ---------------- #

    # Email Domain Validation
    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domains = [
            "axis.com",
            "bob.com",
            "rbi.com",
        ]

        domain_name = value.split("@")[-1]

        if domain_name not in valid_domains:
            raise ValueError("Email domain is not valid")

        return value

    # Convert Name to Uppercase
    @field_validator("name")
    @classmethod
    def name_validator(cls, value):
        return value.upper()
    # ---------------- computed field ---------------- #
    @computed_field
    @property
    def bmi(self) ->float:
        bmi = self.weight/self.height**2
        return round(bmi,2)

    # ---------------- MODEL VALIDATOR ---------------- #

    @model_validator(mode="after")
    def emergency_contact_validator(self):
        if (
            self.age > 60
            and "emergency" not in self.contact_details
        ):
            raise ValueError(
                "Patients older than 60 must have an emergency contact"
            )

        return self


# ---------------- FUNCTIONS ---------------- #

def insert_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("Data inserted successfully")


def update_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("bim of petient",patient.bmi)
    print("Address",patient.address)
    print("Data updated successfully")


# ---------------- INPUT DATA ---------------- #
address_data = {"city":"bhalur","taluka":"nandgaon","state":"maharashtra","pincode":423106}
address_obj = Address(**address_data)



patient_data = {
    "name": "Ishwar",
    "email": "ishwarlahire2004@bob.com",
    "age": 62,
    "linkedin": "https://www.ishwarlahire.com",
    "weight": 69.0,
    "height":4,
    "contact_details": {
        "Phone": "1234567890",
        "emergency": "1122334455",
    },
    "address":address_obj,
}

patient1 = Patient(**patient_data)

insert_data(patient1)
update_data(patient1)

#serilization  export data

temp_data = patient1.model_dump()
temp_data_json = patient1.model_dump_json()
print(temp_data)
print(temp_data_json)

#include exclude
temp_data1 = patient1.model_dump(include="name,email,age") #field only include 


temp_data_json1 = patient1.model_dump_json(exclude="email,name") # field excluded from export data
temp_secure = patient1.model_dump(exclude_unset=True)# for non entered field

print(temp_data1)
print(temp_data_json1)
print("==============================================")
print(type(temp_data_json))
print(temp_data_json)