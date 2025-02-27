from fastapi import FastAPI

from src.config.app_config import create_app, get_custom_openapi
from src.config.swagger_config import config_swagger, delete_router_tag, get_routes
from src.settings import settings


app = create_app(
    docs_url=None,
    redoc_url=None,
)

app.openapi = get_custom_openapi(app)
config_swagger(app, settings.app.APP_TITLE)


######################################################################

delete_router_tag(app)


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
