from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def  hello():
    return {"message":"hello from fastAPI This is a first app"}

@app.get("/about")
def about():
    return{"message":"This is a fast API application"}