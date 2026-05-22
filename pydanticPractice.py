from typing import Annotated, List, Optional
from pydantic import (
    AnyUrl,
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)
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
    print("Data updated successfully")


# ---------------- INPUT DATA ---------------- #

patient_data = {
    "name": "Ishwar",
    "email": "ishwarlahire2004@bob.com",
    "age": 62,
    "linkedin": "https://www.ishwarlahire.com",
    "weight": 69.0,
    "contact_details": {
        "Phone": "1234567890",
        "emergency": "1122334455",
    },
}


# ---------------- OBJECT CREATION ---------------- #

patient1 = Patient(**patient_data)

insert_data(patient1)
update_data(patient1)