from fastapi import FastAPI

app = FastAPI()

@app.get("/test")
async def hello():
    return {"Hello": "World"}