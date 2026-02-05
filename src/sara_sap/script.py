import uvicorn
from sara_sap.settings import settings


def start():
    uvicorn.run(
        "sara_sap.api:app", host=settings.API_HOST_IP, port=settings.PORT, reload=True
    )


if __name__ == "__main__":
    start()
