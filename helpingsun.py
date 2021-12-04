
from datetime import datetime
import pickle

def get_datetime():
    time =str(datetime.now().time())[:5]
    if int(time[:2]) < 12:
        time = time + " AM"
    else:
        hour = int(time[:2]) - 12
        mini = time[3:]
        if hour < 10:
            time = '0' +str(hour) + ":"+ mini + " PM"    
        else:    
            time = '0' +str(hour) + ":"+ mini + " PM"           
    fdate = str(datetime.now().date())
    year = fdate[:4]
    month_list = ["January" , "February" , "March" , "April" , "May" , "June" , "July" , "August" , "September" , "October" , "November" , "December"]
    month =  month_list[int(fdate[5:7])-1]   
    date = fdate[8:]
    date = date + "-" + month + "-" + year
    return time , date
    

def get_data(id = 0):
    # print("get_data" , id)
    with open('postDictionary.pickle', 'rb') as f:
        sample =pickle.load(f)
    data =[]
    for i in sample:
        i["likes"] = get_likes_by_post_id(i["id"])
        if i["likes"] == False:
            i["likes"] = 0
        data.append(i)
    if id==0:
        return data
    else:
        for i in data:
            if id == i['id']:
                # print("succees")
                return i
    return False

def write_data(data):
    print("writing data" ,data)
    with open('postDictionary.pickle', 'wb') as f:
        pickle.dump(data, f ,pickle.HIGHEST_PROTOCOL)
        
def check_user(username):
    with open('users.pickle', 'rb') as f:
        sample =pickle.load(f)
    for i in sample:
        if username == i['username']:
            return False
    return True


def get_pass_username(username):
    with open('users.pickle', 'rb') as f:
        sample =pickle.load(f)
    for i in sample:
        if username == i['username']:
            return i['password']
    assert("wrong in get_pass_username")
    
def get_pass_email(email):
    with open('users.pickle', 'rb') as f:
        sample =pickle.load(f)
    for i in sample:
        if email == i['email']:
            return i['password']
    assert("wrong in get_pass_mail")


def check_user_bymail(email):
    with open('users.pickle', 'rb') as f:
        sample =pickle.load(f)
    for i in sample:
        if email == i['email']:
            return False
    return True

def get_user(username):
    with open('users.pickle', 'rb') as f:
        sample =pickle.load(f)
    for i in sample:
        if username == i['username']:
            return i
    return False

def get_alluser():
    with open('users.pickle', 'rb') as f:
        sample =pickle.load(f)
    return sample

def insert_user(username,password ,email ,name):
    # sample_dict = {'username':'rahul99', 'password':'rahul', 'name': 'rahul', 'date':d,  'email':'rahul@rt.t' }
    status=check_user(username)
    # password =  cryptocode.encrypt(password,"enc")
    # print("insertuinf pass" , password)
    if status:
        with open('users.pickle', 'rb') as f:
            sample =pickle.load(f)
        t, d = get_datetime()
        sample.append({'username':username , 'password':password ,    'email':email , 'name':name, 'date':d })
        with open('users.pickle', 'wb') as f:
            pickle.dump(sample, f ,pickle.HIGHEST_PROTOCOL)
        # print("inserted user success : ", username )
        return True
    else :
        # print("user already exist")
        return False
    
    
def get_all_post_by_user(username):
    # print("valid user :",check_user(username))
    if check_user(username)==False:
        with open('postDictionary.pickle', 'rb') as f:
            sample =pickle.load(f)
        post_list = []
        for i in sample:
            if i['user_id'] == username:
                post_list.append(i)
        return post_list
    else:
        return False
    

def set_likes_by_post_id(post_id , username):
    
    
    #  retrun parameter :   0 :success like , 1 : already liked , 2 : post not found
    
    try:
        username = username['username']
    except Exception as e:
        print(e)
        return "Excpetion has occured"
    print("user {} linked to post {}".format(username,post_id))
    with open('likes.pickle', 'rb') as f:
        sample =pickle.load(f)
    for i in sample:
        # print(i)
        if i["post_id"] == str(post_id):
            print("post_id liked by :", i["liked_users"])
            if username not in i["liked_users"]:
                # print("user not in list inserting username ", username) 
                i["liked_users"].append(username)
                # print("post {} liked by {}".format(post_id,i["liked_users"]))
                with open('likes.pickle', 'wb') as f:
                    pickle.dump(sample , f ,pickle.HIGHEST_PROTOCOL)
                return 0
            else:
                i["liked_users"].pop(i["liked_users"].index(username))
                with open('likes.pickle', 'wb') as f:
                    pickle.dump(sample , f ,pickle.HIGHEST_PROTOCOL)
                return 1
    return 2

def get_likes_by_post_id(post_id):
    with open('likes.pickle', 'rb') as f:
        sample =pickle.load(f)
    # print("postid :",post_id)
    for i in sample:
        # print("inn i :",i)
        if i["post_id"] == str(post_id):
            total_likes = len(i["liked_users"])
            # print("post present with like ", total_likes)
            return total_likes
    return False


def insert_post_entry_in_likes(post_id):
    with open('likes.pickle', 'rb') as f:
        sample =pickle.load(f)
    sample.append({'post_id':str(post_id) , 'liked_users':[]})
    with open('likes.pickle', 'wb') as f:
        pickle.dump(sample, f ,pickle.HIGHEST_PROTOCOL)
        
    print("inserted post_id in likes")
    