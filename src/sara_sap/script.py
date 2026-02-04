import uvicorn


def start():
    uvicorn.run("sara_sap.api:app", host="0.0.0.0", port=3017, reload=True)


if __name__ == "__main__":
    start()
