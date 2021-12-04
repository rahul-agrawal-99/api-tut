import pickle
from datetime import datetime
#  format 
from helpingsun import *
#  [{post_id : [liked user id ]}]


# with open('likes.pickle', 'wb') as f:
#   pickle.dump([ {"post_id":"598929" ,"liked_users": [ 'rahul']}] , f ,pickle.HIGHEST_PROTOCOL)
  
with open('postDictionary.pickle', 'wb') as f:
  pickle.dump([] , f ,pickle.HIGHEST_PROTOCOL)

# print(get_likes_by_post_id("506860"))

# with open('likes.pickle', 'rb') as f:
#     sample =pickle.load(f)
    
with open('postDictionary.pickle', 'rb') as f:
    sample =pickle.load(f)
    
print(sample)