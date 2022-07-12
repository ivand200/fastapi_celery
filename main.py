from fastapi import FastAPI


from worker import send_notifictions

app = FastAPI()

@app.get("/test")
async def telegram():
    """
    Task: send telegram notification
    """
    result = send_notifictions.delay()
    return {"status": "ok"}