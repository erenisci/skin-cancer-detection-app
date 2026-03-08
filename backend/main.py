from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from internal.exception.base_exception import BaseException
from internal.exception.handler import (base_exception_handler,
                                        generic_exception_handler,
                                        http_exception_handler,
                                        validation_exception_handler)
from routes import report_controller
from routes.auth_controller import router as auth_router
from routes.detection import router as detection_router
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.add_exception_handler(BaseException, base_exception_handler)
app.include_router(auth_router)
app.include_router(detection_router)
app.include_router(report_controller.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Skin Cancer Detection App!"}


app.mount("/", StaticFiles(directory="static", html=True), name="static")
