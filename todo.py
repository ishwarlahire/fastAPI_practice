from fastapi import FastAPI
from pydantic import BaseModel,EmailStr

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


@app.put("/update")
def update(id:int,data_update:Todo):
    for index,data in enumerate(Todos):
        if data.id == id:
            Todos[index]=data_update
            return {
                "message":"data updated successfully",
                "data":data_update
            }
    return{
        "error":"record not found"
    }

@app.delete("/delete")
def delete(id:int):
    for index,data in enumerate(Todos):
        if data.id == id:
            Todos.pop(index)
            return{
                "message":"record delete successfully",
                "data":Todos
            }
    return{
        "error":"record not found"
    }


 #path , Query , body 

users = []
class User(BaseModel):
        name:str
        age:int
        email:EmailStr

@app.post("/createUser")
def createUser(user:User):
    users.append(user)
    # users.append(12)
    return{
        "message":"user created",
        "data":user
    }

@app.put("/updateUser{user_id}")
def updateUser(user_id:int,user:User,notify:bool = False):
    if user_id<len(users):
        users[user_id] = user
        
        return{
            "message":"user updated ",
            "notify": notify,
            "data":user
        }
    return{
        "error":"user not found"
    }