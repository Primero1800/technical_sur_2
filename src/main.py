import uvicorn

from src.utils import temp
from src.config import app_config
from src.config import swagger_config
from src.settings import settings


app = app_config.create_app(
    docs_url=None,
    redoc_url=None,
)

app.openapi = app_config.get_custom_openapi(app)
swagger_config.config_swagger(app, settings.app.APP_TITLE)

app.include_router(temp.router, tags=[settings.tags.TECH_TAG,])


######################################################################

swagger_config.delete_router_tag(app)
app_config.config_validation_exception_handler(app)


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
    return await swagger_config.get_routes(
        application=app,
    )


if __name__ == "__main__":
    # uvicorn src.main:app --host 0.0.0.0 --reload
    uvicorn.run("src.main:app", host="0.0.0.0", reload=True)
