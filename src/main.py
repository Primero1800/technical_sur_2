import uvicorn
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.responses import JSONResponse

from src.utils import temp
from src.config.app_config import create_app, get_custom_openapi
from src.config.swagger_config import config_swagger, delete_router_tag, get_routes
from src.settings import settings


app = create_app(
    docs_url=None,
    redoc_url=None,
)

app.openapi = get_custom_openapi(app)
config_swagger(app, settings.app.APP_TITLE)

app.include_router(temp.router, tags=[settings.tags.TECH_TAG,])


######################################################################

delete_router_tag(app)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=settings.app.APP_422_CODE_STATUS,
        content={"detail": exc.errors(), "body": exc.body},
    )


@app.get('/', tags=[settings.tags.ROOT_TAG,])
@app.get(
    '', tags=[settings.tags.ROOT_TAG,], include_in_schema=False
)
def top():
    return 'top here'


@app.get("/echo/{thing}/", tags=[settings.tags.TECH_TAG,])
@app.get(
    "/echo/{thing}", tags=[settings.tags.TECH_TAG,], include_in_schema=False
)
def echo(thing):
    return ' '.join([thing for _ in range(3)])


@app.get("/test/", tags=[settings.tags.TECH_TAG])
@app.get(
    "/test", tags=[settings.tags.TECH_TAG], include_in_schema=False
)
def test_endpoint():
    return {"message": "Hello from test!"}


@app.get("/routes/", tags=[settings.tags.TECH_TAG,])
@app.get(
    "/routes", tags=[settings.tags.TECH_TAG,], include_in_schema=False
)
async def get_routes_endpoint():
    return await get_routes(
        application=app,
    )


if __name__ == "__main__":
    # uvicorn src.main:app --host 0.0.0.0 --reload
    uvicorn.run("src.main:app", host="0.0.0.0", reload=True)
