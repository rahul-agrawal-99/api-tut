
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel # for validation of data, if not in proper format, 
                            #   it will throw error





class Item(BaseModel):   # mentioned only accepted data type with name of data
    title : str
    discription : Optional[str] = "no discription available "
    postdata : Optional[bool] = True
    
    
class User(BaseModel):   # mentioned only accepted data type with name of data
    username : str
    password: str
    name: str
    email: str
    
    
class login(BaseModel):   # mentioned only accepted data type with name of data
    username :Optional[str] = "none"
    email: Optional[str] = "none"
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: Optional[str] = None
