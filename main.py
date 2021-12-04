#   to run file use : uvicorn main:app --reload   main is file name of python file

from typing import List, Optional

from fastapi import FastAPI

import pickle
from pydantic import BaseModel # for validation of data, if not in proper format, 
                            #   it will throw error


class Item(BaseModel):   # mentioned only accepted data type with name of data
    name: str
    aboutyou: Optional[str] = "You are Fool"
    age: int
    byear: Optional[int] = None
    choise: Optional[List[str]] = []
    
# available posts in dictionary
with open('faceDictionary.pickle', 'rb') as f:
    facedic =pickle.load(f)
    

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


# craeting a post request

@app.post("/post")
def posts(data : dict):  # data type should be mentioned in the post request for json use dict
    print("data is " , data)
    return {"data": data}


# craeting a post request with defined data type of class Item
# here we are using pydantic to validate the data , if not in proper format it will throw error
@app.post("/postitem")
def posts(data :  Item):  # data type should be mentioned in the post request for json use dict with validation
    print("data is " , data)
    #  Accepted data type with name of data with post request
    
#     {
#     "name":"rahul",
#     "age": 20,
#     "choise": ["hii" , 45 , true]

# }
    data = data.dict() # converting data to dictionary
    return {"data": data}