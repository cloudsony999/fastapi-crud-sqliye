import models
from db import engine
from db import SessionLocal
#import crud to give access to the operations that we defined
import crud
from fastapi import FastAPI
from sqlalchemy.orm import Session

#initailize FastApi instance
app = FastAPI()



#create the database tables on app startup or reload
models.Base.metadata.create_all(bind=engine)


#define endpoint
@app.get("/")
def home():
    return {"amitava": "FastApi Teacher"}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""
So that FastAPI knows that it has to treat a variable as a dependency,
we will import Depends
"""
from fastapi import Depends



#define endpoint
@app.post("/create_friend")
def create_friend(first_name:str, last_name:str, age:int, db:Session = Depends(get_db)):
    friend = crud.create_friend(db=db, first_name=first_name, last_name=last_name, age=age)
##return object created
    return {"friend": friend}


@app.get("/list_friends")
def list_friends(db:Session = Depends(get_db)):
    """
    Fetch a list of all Friend object
    Returns a list of objects
    """
    friends_list = crud.list_friends(db=db)
    return friends_list

@app.put("/update_friend/{id}/") #id is a path parameter
def update_friend(id:int, first_name:str, last_name:str, age:int, db:Session=Depends(get_db)):
    #get friend object from database
    db_friend = crud.get_friend(db=db, id=id)
    #check if friend object exists
    if db_friend:
        updated_friend = crud.update_friend(db=db, id=id, first_name=first_name, last_name=last_name, age=age)
        return updated_friend
    else:
        return {"error": f"Friend with id {id} does not exist"}
    
@app.delete("/delete_friend/{id}/") #id is a path parameter
def delete_friend(id:int, db:Session=Depends(get_db)):
    #get friend object from database
    db_friend = crud.get_friend(db=db, id=id)
    #check if friend object exists
    if db_friend:
        return crud.delete_friend(db=db, id=id)
    else:
        return {"error": f"Friend with id {id} does not exist"}
    
