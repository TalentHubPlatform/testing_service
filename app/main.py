from create_fastapi_app import init_app
from uvicorn import run

app = init_app()

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", reload=True, port=8000)
