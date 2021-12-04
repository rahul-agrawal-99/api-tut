#   to run file use : uvicorn app1:app --reload   main is file name of python file

from typing import List, Optional
from fastapi.params import Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import FastAPI , Response ,Request , HTTPException
from datetime import datetime
import pickle
import random

from starlette.responses import RedirectResponse
from helpingsun import *
from schema import *
from auth import *
import re
from config import *
                            
#  hasing password
# import cryptocode



app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(token: str = Depends(oauth2_scheme)):
    # print("inside get_current_user token :", token)
    # var = HTTPException(status_code=401, detail="Not authorized")
    
    decoded_token = verify_access_token(token)
    # print("decoded_token: ", decoded_token)
    #  return current user
    if decoded_token == False:
        return False
    var = HTTPException(status_code=200, detail=f"authorized user {decoded_token.get('username')} ")
    return decoded_token


'''
INDEX PAGE
'''


@app.get("/" , response_class=HTMLResponse)
def read_root():
    return "heloo this is index page"

@app.post("/login" , response_model=Token)
def login(data : OAuth2PasswordRequestForm = Depends()): 
    # print("login data:",data)
    if not check_user_bymail(data.username):   # if no username is given
        password = get_pass_email(data.username)
        authenticate = verify_password(data.password, password)
        if authenticate:
            token = create_access_token({ 'username' : data.username  })
            return {"access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=404, detail=f"wrong password usinfg mail")
        
    if not check_user(data.username):   # if no username is given
        password = get_pass_username(data.username)
        authenticate = verify_password(data.password, password)
        if authenticate:
            token = create_access_token({ 'username' : data.username  })
            return {"access_token": token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=404, detail=f"wrong password usinfg username")
    return {"something went wrong ": data}
# @app.post("/login")
# def login(data : OAuth2PasswordRequestForm = Depends()): 
# # def login(data : login): 
#     # data = data.dict()
#     print("login data :",data)
#     if not check_user_bymail(data.username):   # if no username is given
#         print("no email")
#         check_mail = check_user_bymail(data["email"])
#         if check_mail== False:
#             password = get_pass_email(data["email"])
#             if password == data["password"]:
#                 data.pop("username")
#                 data.pop("password")
#                 token = create_access_token(data)
#                 return {"login success with email:" : data["email"] , "Token" : token}
#             raise HTTPException(status_code=404, detail=f"wrong password")
#         else:
#             raise HTTPException(status_code=404, detail=f"email not in db as {data['email']}")
#     elif data["email"] == "none":   # if no email is given
#         print("no email")
#         check_username = check_user(data["username"])
#         if check_username == False:
#             password = get_pass_username(data["username"])
#             if password == data["password"]:
#                 data.pop("email")
#                 data.pop("password")
#                 token = create_access_token(data)
#                 return {"login success with username:" : data , "Token" : token}
#             raise HTTPException(status_code=404, detail=f"wrong password")
#         else:
#             raise HTTPException(status_code=404, detail=f"username not in db as {data['username']}")
#     else:  
#         return {"something went wrong ": data}



'''
RELETED TO POSTS
'''

# get all posts
@app.get("/postall")
def getpost(search : Optional[str] = "none"):  # data type should be mentioned in the post request for json use dict
    posts =get_data()
    data = []
    for i in posts:
        i["likes"] = get_likes_by_post_id(i["id"])
        if i["postdata"] == True:
            data.append(i)
    if search == "none":
        return {"get all post data": data}
    else:
        new_data = []
        print("search :",search)
        substr = search
        for i in data:
            string = i["title"]
            # print("string :",string)
            result = re.search(substr, string, re.IGNORECASE)
            if result:
                new_data.append(i)
            # print("result :",result)
        return {"get all post data with search": new_data}
#  retrurn latest post
@app.get("/post/latest")
def getlatestpost():  # data type should be mentioned in the post request for json use dict
    print("get latest post")
    posts =get_data()
    # print(posts)
    posts.reverse()
    # print("posts",posts)
    return {"get all post data": posts}

# get sigle post with id
@app.get("/post/{id}" )
def get_post(id :int ):
    print("in /post/id")
    posts =get_data(id)
    if posts == False:
        raise HTTPException(status_code=404, detail=f"post not found with id:{id}")
    if posts["postdata"]:
        return {f"get post data with id {id}": posts}
    raise HTTPException(status_code=401, detail=f"Post in not public")


#  get all posts , posted by user
@app.get("/postall/{username}")
def getallpostsbyusername(username : str , current_user  = Depends(get_current_user)):  # data type should be mentioned in the post request for json use dict
    print("current user :",current_user)
    data = get_all_post_by_user(username)
    if current_user == False:
        slave_data = []
        for i in data:
            if i["postdata"] == True:
                    slave_data.append(i)
        return {"current user is": current_user, f"you are visiting '{username}''s data": slave_data}
    try:
        if data != False:
            if username == current_user.get("username"):
                return {"You are Owner": data}
            else:
                slave_data = []
                for i in data:
                    if i["postdata"] == True:
                        slave_data.append(i)
                return {"current user is": current_user, f"you are visiting '{username}''s data": slave_data}
    except Exception as e:
        return "error with credential please relogin current user is '{}'".format(current_user) 
    raise HTTPException(status_code=404, detail="user not found")




@app.get("/post/like/{post_id}")
def getlatestpost(post_id : int , current_user  = Depends(get_current_user)):  # data type should be mentioned in the post request for json use dict
    print("inside post like id ",post_id)
    posts =set_likes_by_post_id(post_id , current_user)
    likes = get_likes_by_post_id(post_id)
    if posts == 0:
        return {f"like on post with id [{post_id}] :": likes}
    elif posts == 1:
        return {f"dislike on post with id [{post_id}] are :": likes }
    elif posts == 2:
        raise HTTPException(status_code=404, detail="post not found")    
    else:
        raise HTTPException(status_code=403, detail="Error occured")





# # get sigle post with id
# @app.get("/post/{id}" )
# def get_post(id : int ):
#     posts =get_data(id)
#     if posts == False:
#         raise HTTPException(status_code=404, detail=f"post not found with id:{id}")
#     return {f"get post data with id {id}": posts}

#  post a new post
@app.post("/post" , status_code=201 )
def postposts(data :  Item  , current_user  = Depends(get_current_user)):  # data type should be mentioned in the post request for json use dict with validation
    print("cuuerent user:",current_user)
    data = data.dict() # converting data to dictionary
    print(data)
    try:
        data["user_id"] = current_user['username']
    except Exception as e:
        return {"error": e , 'current user': current_user}
    data['id'] = random.randrange(1,999999)
    time , date =get_datetime()
    data['date'] = date
    data['time'] = time
    posts =get_data()
    posts.append(data)
    write_data(posts)
    insert_post_entry_in_likes(data['id'])
    # response.status_code = 201
    return {"saved data as": data}

# update post
@app.put("/post/{id}")
def update_post(data : Item,id : int , response : Response , current_user  = Depends(get_current_user)):
    posts =get_data(id)
    response.status_code = 201
    if posts == False:
        response.status_code = 404
        return {"error": "post not found"}
    posts =get_data()
    data = data.dict()
    for index, i in enumerate(posts):
        if id == i['id']:
            if i["user_id"] == current_user['username']:
                data['user_id'] = current_user['username']
                data['id'] = id
                time , date =get_datetime()
                data['date'] = date
                data['time'] = time
                posts[index]=data
                write_data(posts)
                return {"updated data": get_data(id)}
            else:
                raise HTTPException(status_code=401, detail="you are not owner of this post")
    response.status_code = 404
    return {"error": "something went wrong"}
    

#  delete a single post item
@app.delete("/post/{id}" )
def deletepost(id : int , response : Response , current_user  = Depends(get_current_user)):
    post =get_data(id)
    if post == False:
            response.status_code = 404
            return {"error": f"post not found with ID = {id}"}
    print("posts ",post)
    if post['user_id'] ==current_user['username']:
        posts =get_data()
        for index, i in enumerate(posts):
            if id == i['id']:
                posts.pop(index)
                write_data(posts)
                response.status_code = 204
                return {"suceess ": f"post deleted with ID = {id}" ,"posts":post}
    response.status_code = 403
    return {"error": "You dont have access to delete this post" , 'post belongs to ' : post['user_id'] , 'current user' : current_user}



'''
RELETED TO USER
'''

#  get user details by username
@app.get("/user/{username}")
def getuserdetails(username : str):  # data type should be mentioned in the post request for json use dict
    isuser = check_user(username)
    print("*****",isuser)
    if isuser == False:
        details = get_user(username)
        data ={}
        data['username'] = details['username']
        data['name'] = details['name']
        data['email'] = details['email']
        data['user_created'] = details['date']
        return {"user details": data}
    return HTTPException(status_code=404, detail="user not found")

#  get all users details
@app.get("/getalluser")
def getpost():  # data type should be mentioned in the post request for json use dict
    posts =get_alluser()
    return {"get all post data": posts}


#  insert new user
@app.post("/insertuser" , status_code=201)
def insertuser(data :  User , response : Response ):  # data type should be mentioned in the post request for json use dict with validation
    # data = data.dict() # converting data to dictionary
    data.password = generate_password_hash(data.password)
    
    st =insert_user(data.username,data.password ,data.email,data.name)
    if st == True:
        return {"inserted user  as": get_user(data.username)}
    else:
        response.status_code = 404
        print("user already exist")
        return {"SOS": "user already exist"}

