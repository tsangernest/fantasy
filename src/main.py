from fastapi import FastAPI


def get_application() -> FastAPI:
    application = FastAPI(debug=True)
    return app


app = get_application()

