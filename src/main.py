import uvicorn

from src.utils import temp
from src.core.config import AppConfigurer, SwaggerConfigurer
from src.core.settings import settings
from src.api_v1 import router as router_v1


app = AppConfigurer.create_app(
    docs_url=None,
    redoc_url=None,
)

app.openapi = AppConfigurer.get_custom_openapi(app)

app.include_router(
    router_v1,
    prefix=settings.app.API_V1_PREFIX,
)
app.include_router(
    temp.router,
    prefix="/temp",
    tags=[
        settings.tags.TECH_TAG,
    ],
)


SwaggerConfigurer.config_swagger(app, settings.app.APP_TITLE)


######################################################################

SwaggerConfigurer.delete_router_tag(app)
AppConfigurer.config_validation_exception_handler(app)


@app.get("/", tags=[settings.tags.ROOT_TAG,],)
@app.get("", tags=[settings.tags.ROOT_TAG,], include_in_schema=False,)
def top():
    return "top here"


@app.get("/echo/{thing}/", tags=[settings.tags.TECH_TAG,],)
@app.get("/echo/{thing}", tags=[settings.tags.TECH_TAG,], include_in_schema=False,)
def echo(thing):
    return " ".join([thing for _ in range(3)])


@app.get("/test/", tags=[settings.tags.TECH_TAG])
@app.get("/test", tags=[settings.tags.TECH_TAG], include_in_schema=False)
def test_endpoint():
    return {"message": "Hello from test!"}


@app.get("/routes/", tags=[settings.tags.TECH_TAG,],)
@app.get("/routes",  tags=[settings.tags.TECH_TAG,], include_in_schema=False,)
async def get_routes_endpoint():
    return await SwaggerConfigurer.get_routes(
        application=app,
    )


if __name__ == "__main__":
    # gunicorn app1.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
    # uvicorn src.main:app --host 0.0.0.0 --reload
    uvicorn.run("src.main:app", host="0.0.0.0", reload=True)
