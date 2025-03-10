from src.core.settings import settings
from src.core.gunicorn import get_app_options, GunicornApplication
from src.main import app as app


def main():
    gunicorn_app = GunicornApplication(
        app=app,
        options=get_app_options(
            host=settings.app.APP_HOST,
            port=settings.app.APP_PORT,
            workers=settings.gunicorn.WORKERS,
            timeout=settings.gunicorn.TIMEOUT,
        )
    )
    gunicorn_app.run()



if __name__ == "__main__":
    main()