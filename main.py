from fastapi import FastAPI
import dataset

app = FastAPI()

db = dataset.connect("sqlite:///teal.sqlite")
user = db["user"]
tweet = db["tweet"]


@app.get("/view")
def viewAllTweet():
    return {"message": "view!"}

@app.get("/view/{user_id}/{tweet_id}")
def viewTweet(user_id: str, tweet_id: int):
    return {"user_id": user_id, "tweet_id": tweet_id}

@app.get("/user/{user_id}")
def userProfile(user_id: str):
    userData = user.find(userid=user_id)
    return {"userData": userData}

@app.post("/signup")
def signUp(email: str, password: str, userid: str):
    try:
        user.insert({"email": email, "password": password, "userid": userid, "detail": None})
        return {"result": "success"}
    except:
        return {"result": "error"}

@app.post("/new")
def newTweet(email: str, password: str, tweet: str):
    return {"email": email, "password": password, "tweet": tweet}

@app.post("/reply/{user_id}/{tweet_id}")
def replyTweet(user_id: str, tweet_id: int, email: str, password: str, reply: str):
    return {"user_id": user_id, "tweet_id": tweet_id, "email": email, "password": password, "reply": reply}

@app.post("/user/{user_id}")
def changeProfile(user_id: str, email: str, password: str, detail: str):
    return {"user_id": user_id, "email": email, "password": password, "detail": detail}

@app.post("/delete/tweet/{user_id}/{tweet_id}")
def deleteTweet(user_id: str, tweet_id: int, email: str, password: str):
    return {"user_id": user_id, "tweet_id": tweet_id, "email": email, "password": password}

@app.post("/delete/user/{user_id}")
def deleteUser(user_id: str, email: str, password: str):
    return {"user_id": user_id, "email": email, "password": password}


