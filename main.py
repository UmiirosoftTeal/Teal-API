from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import dataset
import datetime as dt
import pytz
import hashlib as hl


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = dataset.connect("sqlite:///teal.sqlite")
user = db["user"]
tweet = db["tweet"]


@app.get("/view")
def viewAllTweet():
    try:
        data = tweet.find()
        text = []
        for d in data:
            text.append(d)
        return text
    except:
        return {"result": "None"}


@app.get("/view/{user_id}")
def viewUserTweet(user_id: str):
    try:
        data = tweet.find(userid=user_id)
        text = []
        for d in data:
            text.append(d)
        return text
    except:
        return {"result": "None"}


@app.get("/view/{user_id}/{tweet_id}")
def viewUserTweet(user_id: str, tweet_id: int):
    try:
        data = tweet.find(userid=user_id, id=tweet_id)
        text = []
        for d in data:
            text.append(d)
        return text
    except:
        return {"result": "None"}


@app.get("/user/{user_id}")
def userProfile(user_id: str):
    try:
        userData = user.find_one(userid=user_id)
        return {"id": userData["id"], "userid": userData["userid"], "icon_url": userData["icon_url"], "detail": userData["detail"]}
    except:
        return {"result": "None"}


@app.get("/users")
def viewAllUser():
    try:
        data = user.find()
        users = []
        for d in data:
            x = {"id": d["id"], "userid": d["userid"], "icon_url": d["icon_url"], "detail": d["detail"]}
            users.append(x)
        return users
    except:
        return {"result": "None"}
      

@app.post("/signup")
def signUp(email: str, password: str, userid: str):
    try:
        icon_md5 = hl.md5(email.encode()).hexdigest()
        icon = "https://www.gravatar.com/avatar/" + icon_md5 + "?s=1000"
        password = hl.sha256(password.encode()).hexdigest()
        user.insert({"email": email, "password": password,
                    "userid": userid, "icon_url": icon, "detail": ""})
        return {"result": "POST"}
    except:
        return {"result": "None"}


@app.post("/new")
def newTweet(email: str, password: str, text: str):
    try:
        userData = user.find_one(email=email)
        password = hl.sha256(password.encode()).hexdigest()
        if userData["password"] == password:
            userid = userData["userid"]
            nowDate = dt.datetime.now(pytz.timezone('Asia/Tokyo'))
            icon_md5 = hl.md5(email.encode()).hexdigest()
            icon = "https://www.gravatar.com/avatar/" + icon_md5 + "?s=1000"
            tweet.insert({"userid": userid, "tweet": text,
                         "to": None, "icon_url": icon, "date": nowDate, "like": 0})
            return {"result": "POST"}
    except:
        return {"result": "None"}


@app.post("/reply/{user_id}")
def replyTweet(user_id: str, email: str, password: str, reply: str):
    try:
        userData = user.find_one(email=email)
        password = hl.sha256(password.encode()).hexdigest()
        if userData["password"] == password:
            userid = userData["userid"]
            nowDate = dt.datetime.now(pytz.timezone('Asia/Tokyo'))
            icon_md5 = hl.md5(email.encode()).hexdigest()
            icon = "https://www.gravatar.com/avatar/" + icon_md5 + "?s=1000"
            tweet.insert({"userid": userid, "tweet": reply,
                         "to": user_id, "icon_url": icon, "date": nowDate, "like": 0})
            return {"result": "POST"}
    except:
        return {"result": "None"}


@app.post("/like/{tweet_id}")
def likeTweet(tweet_id: int):
    try:
        tweetData = tweet.find_one(id=tweet_id)
        newLike = tweetData["like"] + 1
        tweet.update({"id": tweet_id, "like": newLike}, ["id"])
        return {"result": "POST"}
    except:
        return {"result": "None"}


@app.post("/user/{user_id}")
def changeProfile(user_id: str, email: str, password: str, detail: str):
    try:
        userData = user.find_one(email=email)
        password = hl.sha256(password.encode()).hexdigest()
        if userData["password"] == password:
            user.update({"userid": user_id, "detail": detail}, ["userid"])
            return {"result": "POST"}
    except:
        return {"result": "None"}


@app.post("/delete/tweet/{user_id}/{tweet_id}")
def deleteTweet(user_id: str, tweet_id: int, email: str, password: str):
    try:
        userData = user.find_one(email=email)
        password = hl.sha256(password.encode()).hexdigest()
        if userData["password"] == password:
            tweet.delete(userid=user_id, id=tweet_id)
            return {"result": "POST"}
    except:
        return {"result": "None"}


@app.post("/delete/user/{user_id}")
def deleteUser(user_id: str, email: str, password: str):
    try:
        userData = user.find_one(email=email)
        password = hl.sha256(password.encode()).hexdigest()
        if userData["password"] == password:
            tweet.delete(userid=user_id)
            user.delete(userid=user_id)
            return {"result": "POST"}
    except:
        return {"result": "None"}

