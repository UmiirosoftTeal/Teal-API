from fastapi import FastAPI

app = FastAPI()

@app.get("/view")
async def root():
    return {"message":"view!"}
