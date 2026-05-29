from fastapi import FastAPI,status,HTTPException
from pydantic import BaseModel, EmailStr
from fastapi.responses import JSONResponse

app = FastAPI()

Todos = []

class Todo(BaseModel):
    id: int
    title: str
    completed: bool


@app.post("/create")
def create_todo(todo: Todo):
    Todos.append(todo)
    return {
        "message": "Task added in list",
        "todo": todo
    }


@app.get("/getAllTasks")
def get_all_tasks():
    return {
        "message": "Fetch all task data",
        "data": Todos
    }


@app.get("/getbyid")
def get_by_id(id: int):
    for record in Todos:
        if record.id == id:
            return {
                "message": "Record fetched successfully",
                "data": record
            }
    return {"message": "Record not found"}


@app.put("/update")
def update(id: int, data_update: Todo):
    for index, data in enumerate(Todos):
        if data.id == id:
            Todos[index] = data_update
            return {
                "message": "Data updated successfully",
                "data": data_update
            }
    return {
        "error": "Record not found"
    }


@app.delete("/delete")
def delete(id: int):
    for index, data in enumerate(Todos):
        if data.id == id:
            Todos.pop(index)
            return {
                "message": "Record deleted successfully",
                "data": Todos
            }
    return {
        "error": "Record not found"
    }


users = []

class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    name: str
    age: int
    email: EmailStr


class GetUsersResponse(BaseModel):
    message: str
    data: list[UserResponse]


@app.post("/createUser")
def create_user(user: User):
    users.append(user)
    return {
        "message": "User created",
        "data": user
    }


@app.put("/updateUser/{user_id}")
def update_user(user_id: int, user: User, notify: bool = False):
    if user_id < len(users):
        users[user_id] = user
        return {
            "message": "User updated",
            "notify": notify,
            "data": user
        }
    else:
        raise HTTPException(status_code=409,detail="record not found / bad request")
   


@app.get("/getusers", status_code=status.HTTP_200_OK, response_model=GetUsersResponse)
def get_users():
    return {
        "message": "Fetch data successfully",
        "data": users
    }

@app.get("/missingUser/{name}")
def missingUser(name:str):
    for user in users:
        if user.name == name:
            return JSONResponse(
            status_code=200,
            content={
                "message":"user found",
                "data":user.model_dump()
            }
        )
    return JSONResponse(
        status_code=404,
        content={
            "message":"user not found"
        }
    )

class UserNotFOundException(Exception):
    def __init__(self, *name):
        self.name = name
    
@app.get("selfException/{name}")
def selfException(name:str):
    if name !="om":
        return JSONResponse(
            status_code=404,
            content={
                "message":"user not found"
            }
        )
    return JSONResponse(
        status_code=200,
        content={
            "message":"user found",
            "data":"ishwar"
        }
    )