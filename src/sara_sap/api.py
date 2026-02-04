from fastapi import FastAPI


def setup_fastapi() -> FastAPI:
    app = FastAPI()

    @app.get("/")
    async def read_root():
        return {"Hello": "World"}

    return app


app = setup_fastapi()
