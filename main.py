# Python
from ast import For
from collections import UserDict
from email import message
import json
from uuid import UUID
from datetime import date
from datetime import datetime
from typing import Optional, List

# Pydantic
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field

# FastAPI
from fastapi import Body, Path, Form, FastAPI
from fastapi import status

app = FastAPI()

# Models

class UserBase(BaseModel):
    user_id: UUID = Field(...)
    email: EmailStr = Field(...)

class UserLogin(UserBase):
    password: str = Field(
        ..., 
        min_length=8,
        max_length=64
    )

class User(UserBase):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    birth_date: Optional[date] = Field(default=None)

class Tweet(BaseModel):
    tweet_id: UUID = Field(...)
    content: str = Field(
        ..., 
        min_length=1, 
        max_length=256
    )
    created_at: datetime = Field(default=datetime.now())
    updated_at: Optional[datetime] = Field(default=None)
    by: User = Field(...)

class UserRegistrer(User):
    password: str = Field(
        ..., 
        min_length=8,
        max_length=64
    )

class LoginOut(BaseModel): 
    email: EmailStr = Field(...)
    message: str = Field(default="Login Successfully!")

# Path Operations

## Users

### Register a user
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
)
def signup(user: UserRegistrer = Body(...)): 
    """
    Signup 

    This path operations registrer a user in the app

    Parameters:
        -Request body parameters
            -UserRegistrer
    Returns a json with the basic user information:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("users.json", "r+", encoding="UTF-8") as f:
        results = json.loads(f.read())
        user_dict = user.dict()
        user_dict["user_id"] = str(user_dict["user_id"])
        user_dict["birth_date"] = str(user_dict["birth_date"])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user



### Login a user
@app.post(
    path="/login",
    response_model=LoginOut,
    status_code=status.HTTP_200_OK,
    summary="Login a User",
    tags=["Users"]
)
def login(email: EmailStr = Form(...), password: str = Form(...)): 
    """
    Login

    This path operations login a user in the app

    Parameters:
        -Request body parameters
            - email
            - password
    Returns a json with the basic user information:
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        usuarios = json.loads(f.read())
    for user in usuarios:
        if user["email"] == email and user["password"] == password:
            return LoginOut(email=email)
### Show all users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all users",
    tags=["Users"]
)
def show_all_users(): 
    """
    This Path operations show all users in the app

    Parameters:
        -
    
    Returns a Json list with all users in the app, with the following keys
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """

    with open("users.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results
    
### Show a user
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
)
def show_a_user(user_id: UUID = Path(...)): 
    """
    This Path operations show a users in the app

    Parameters:
        -
    
    Returns a Json user in the app, with the following keys
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """

    with open("users.json", "r", encoding="utf-8") as f:
        usuarios = json.loads(f.read())
        id = str(user_id)
    for user in usuarios:
        if user["user_id"] == id:
            return user 

### Delete a user
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
)
def delete_a_user(user_id: UUID = Path(...)): 
    """
    This Path operations delete a user in the app

    Parameters:
        -
    
    Returns a delete in the app, with the following keys
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    with open("users.json", "r+", encoding="utf-8") as f:
        usuarios = json.loads(f.read())
        id = str(user_id)
    for user in usuarios:
        if user["user_id"] == id:
            usuarios.remove(user)
            with open("users.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(usuarios))
                return user
### Update a user
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
)
def update_a_user(user_id: UUID = Path(
            ...,
            title="User ID",
            description="This is the user ID",
            example="3fa85f64-5717-4562-b3fc-2c963f66afa3"
        ),
        user: User = Body(...)
    ): 
    """
    This Path operations Update a user in the app

    Parameters:
        -
    
    Returns a Update in the app, with the following keys
        - user_id: UUID
        - email: Emailstr
        - first_name: str
        - last_name: str
        - birth_date: datetime
    """
    
    user_dict = user.dict()
    user_id = str(user_id)
    user_dict = user.dict()
    user_dict["user_id"] = str(user_dict["user_id"])
    user_dict["birth_date"] = str(user_dict["birth_date"])

    with open("users.json", "r+", encoding="UTF-8") as f:
        usuarios = json.loads(f.read())
    for usr in usuarios:
        if usr["user_id"] == user_id:
            usuarios[usuarios.index(usr)] = user_dict
            with open("users.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(usuarios))
            return user

## Tweets

### Show  all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all tweets",
    tags=["Tweets"]
)
def home():
    """
    This Path operations show all tweets in the app

    Parameters:
        -
    
    Returns a Json list with all tweets in the app, with the following keys
        - tweet_id: UUID 
        - content: str 
        - created_at: datetime 
        - updated_at: Optional[datetime]
        - by: User 
    """

    with open("tweets.json", "r", encoding="utf-8") as f:
        results = json.loads(f.read())
        return results

### Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweets"]
)
def post(tweet: Tweet = Body(...)): 
    """
    Post a Tweet 

    This path operations post a tweet in the app

    Parameters:
        -Request body parameters
            - tweet: Tweet
    Returns a json with the basic tweet information:
        tweet_id: UUID 
        content: str 
        created_at: datetime 
        updated_at: Optional[datetime]
        by: User 
    """
    with open("tweets.json", "r+", encoding="UTF-8") as f:
        results = json.loads(f.read())
        tweet_dict = tweet.dict()
        tweet_dict["tweet_id"] = str(tweet_dict["tweet_id"])
        tweet_dict["created_at"] = str(tweet_dict["created_at"])
        tweet_dict["updated_at"] = str(tweet_dict["updated_at"])
        tweet_dict["by"]["user_id"] = str(tweet_dict["by"]["user_id"])
        tweet_dict["by"]["birth_date"] = str(tweet_dict["by"]["birth_date"])
        results.append(tweet_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return tweet

### Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweets"]
)
def show_a_tweet(tweet_id: UUID = Path(...)): 
    """
    This Path operations show a tweet in the app

    Parameters:
        -
    
    Returns a Json tweet in the app, with the following keys
        tweet_id: UUID 
        content: str 
        created_at: datetime 
        updated_at: Optional[datetime]
        by: User
    """

    with open("tweets.json", "r+", encoding="utf-8") as f: 
        tweets = json.loads(f.read())
        id = str(tweet_id)
    for tweet in tweets:
        if tweet["tweet_id"] == id:
            return tweet


### Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweets"]
)
def delete_a_tweet(tweet_id: UUID = Path(...)): 
    """
    This Path operations delete a tweet in the app

    Parameters:
        -
    
    Returns a delete in the app, with the following keys
        tweet_id: UUID 
        content: str 
        created_at: datetime 
        updated_at: Optional[datetime]
        by: User
    """
    with open("tweets.json", "r+", encoding="utf-8") as f:
        tweets = json.loads(f.read())
        id = str(tweet_id)
    for tweet in tweets:
        if tweet["tweet_id"] == id:
            tweets.remove(tweet)
            with open("tweets.json", "w", encoding="utf-8") as f:
                f.seek(0)
                f.write(json.dumps(tweets))
                return tweet

### Update a tweet
@app.put(
    path="/tweet/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweets"]
)
def update_a_tweet(
    tweet_id: UUID = Path(
        ...,
        title="Tweet ID",
        description="This is the tweet ID",
        example="3fa85f64-5717-4562-b3fc-2c963f66afa9"
    ),
    content: str = Form(
        ..., 
        min_length=1,
        max_length=256,
        title="Tweet content",
        description="This is the content of the tweet",
    )
): 
    """
    Update Tweet

    This path operation update a tweet information in the app and save in the database

    Parameters:
    - tweet_id: UUID
    - content: str
    
    Returns a json with:
        - tweet_id: UUID
        - content: str 
        - created_at: datetime 
        - updated_at: datetime
        - by: user: User
    """
    tweet_id = str(tweet_id)
    results = read_data("tweets")
    for tweet in results:
        if tweet['tweet_id'] == tweet_id:
            tweet['content'] = content
            tweet['updated_at'] = str(datetime.now())
            overwrite_data("tweets", results)
            return tweet

def read_data(file):
    with open(f"{file}.json", "r+", encoding="utf-8") as f:
        return json.loads(f.read()) # Convertirlo a simil de json

def overwrite_data(file, result):
    with open(f"{file}.json", "w", encoding="utf-8") as f:
        f.seek(0) # Moverte al inicio del archivo
        f.write(json.dumps(result)) # Convirtiendo de una list_dic a un json

def show_data(file, id, info):
    results = read_data(file)
    id = str(id)
    for data in results:
        if data[f"{info}_id"] == id:
            return data