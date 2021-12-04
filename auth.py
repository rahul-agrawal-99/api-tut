from fastapi.exceptions import HTTPException
from fastapi.params import Depends
from jose import jwt ,JWTError
from datetime import datetime, timedelta
from schema import Token
from typing import List, Optional
from fastapi.security import OAuth2PasswordBearer
import cryptocode
from config import *


# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="app1/login")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

sett = get_settings()



ALGORITHM = sett.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = sett.access_token_expire_time
key = sett.encryption_key
SECRET_KEY = sett.secret_key



## And then to decode it:
# decoded = cryptocode.decrypt("jGDm+9uwcGE=*SOGUIbN+4bu94fHO0E3R+g==*PQB2SrKfPDk7AiZIzpd6Lg==*hLnYpJ5MiTV/9s9+Ps1piw==", "enc")

# print(decoded)

def generate_password_hash(password: str):
    return cryptocode.encrypt(password, key)

def verify_password(password: str, hashed_password: str) -> bool:
    decoded = cryptocode.decrypt(hashed_password, key)
    return decoded == password



def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    # print("expires_delta: ", expires_delta)
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
        # print("expire: ", expire)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



def verify_access_token(token: str ):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # print("decoded_token in verfy avcess: ", decoded_token)
        id : str = decoded_token.get("username")
        # print("id: ", id)
        if id is None:
            return False
        return decoded_token
    except JWTError as e:
        print("JWTError: ", e)
        return False

# def get_current_user(token: str = Depends(oauth2_scheme)):
#     print("inside get_current_user token :", token)
#     var = HTTPException(status_code=401, detail="Not authorized")
    
#     decoded_token = verify_access_token(token)
#     print("decoded_token: ", decoded_token)
#     #  return current user
#     if decoded_token == False:
#         return var
#     var = HTTPException(status_code=200, detail=f"authorized user {decoded_token.get('username')} ")
#     return decoded_token




if __name__ == "__main__":
    # data = {
    # #   "username": "123456",
    #   "email": "none",
    #   "password": "string"
    # }
    data = {
    "username": "123456"
    #   "email": "none@gmail.com",
    #   "password": "string"
    }


    print(create_access_token(data))

    tk =create_access_token(data)

    ver = get_current_user()

    print("current user is : ", ver)


