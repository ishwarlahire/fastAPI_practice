from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
Todos=[]

class Todo(BaseModel):
    id:int
    title:str
    complated:bool


@app.post("/create")
def create_todo(todos:Todo):
    Todos.append(todos)
    return{
        "message":"Task added in List",
        "Todos_task":todos
    }

@app.get("/getAllTasks")
def getAllTasks():
    return{
        "Message":"Fetch all task data",
        "Data":Todos
    }

@app.get("/getbyid")
def getDyId(id:int):
    for record in Todos:
        if record.id == id:
            return {
                "message":"record fetch successfully",
                "data":record
                }
    return{"message":"record not found"}