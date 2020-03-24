import logging
import os

import boto3
from fastapi import APIRouter, FastAPI
from pydantic import BaseModel, Field
from starlette.requests import Request
from starlette.responses import RedirectResponse


_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

API_V1_STR = "/api/v1"
PROJECT_NAME = "FastAPI-Hello-World"


app = FastAPI(
    title=PROJECT_NAME,
    docs_url=f"{API_V1_STR}",
    redoc_url=f"{API_V1_STR}/redoc",
    openapi_url=f"{API_V1_STR}/openapi.json",
    openapi_prefix=f"/{os.environ.get('STAGE')}",
)
router = APIRouter()


class HelloWorldInput(BaseModel):
    name: str = Field("World", title="Who to greet.")


class HelloWorldOutput(BaseModel):
    message: str = Field(..., title="Hello {name}!")


@router.get("/hello", response_model=HelloWorldOutput, tags=["Hello World"])
def hello_endpoint(request: Request):
    """
    Hello World!
    * return Hello World!
    """
    return {"message": f"Hello World!"}


@router.post("/hello", response_model=HelloWorldOutput, tags=["Hello World"])
def hello_endpoint(request: Request, inputs: HelloWorldInput):
    """
    Greats you.
    * return Hello Name!
    """
    _LOGGER.info(request.scope)
    return {"message": f"Hello {inputs.name}!"}


@router.get("/whoami", tags=["Whoami"])
def whoami_endpoint(request: Request):
    """
    Boto user
    * return {'UserId': 'string', 'Account': 'string', 'Arn': 'string}
    """
    rtn = dict()
    if aws := request.scope.get("aws"):
        rtn.update({"input": aws.event})

    rtn.update({"message": boto3.client("sts").get_caller_identity()})
    return rtn


@app.get("/ping")
def pong():
    """
    Sanity check.
    This will let the user know that the service is operational.
    And this path operation will:
    * show a lifesign
    """
    return {"ping": "pong!"}


# @app.get("/")
# def home():
#     url = app.url_path_for(API_V1_STR[1:])
#     response = RedirectResponse(url=url)
#     return response


app.include_router(router, prefix=API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "api:app", host="127.0.0.1", port=5000, reload=True, log_level="debug", access_log=True,
    )
elif os.environ.get("AWS_EXECUTION_ENV"):
    from mangum import Mangum

    handler = Mangum(app, enable_lifespan=False)
