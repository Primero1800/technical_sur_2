from typing import Any

import uvicorn.workers
from .logger import GunicornLogger


def get_app_options(
        host: str,
        port: int,
        workers: int,
        timeout: int,
        loglevel: str,

) -> dict[str, Any]:
    return {
        "bind": f"{host}:{port}",
        "workers": workers,
        "worker_class": uvicorn.workers.UvicornWorker,
        'timeout': timeout,
        "accesslog": "-",
        "errorlog": "-",
        "logger_class": GunicornLogger,
        "loglevel": loglevel,

    }
