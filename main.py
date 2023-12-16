import uvicorn
from fastapi import FastAPI

from modules import command

app = FastAPI()


@app.get("/")
def health():

    return {"data": {"health": True}}


@app.get("/ping")
def ping(host, target, source, port = 22):

    result = command.ping(host, target, source, port)

    if result != "fail":
        response = {"data": {"health": True, "success": result}}
    else:
        response = {"data": {"health": True}}

    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, log_level="info")
