from typing import Any

import uvicorn.workers
from fastapi import FastAPI


def get_app_options(
        host: str,
        port: int,
        workers: int,
        timeout: int,
) -> dict[str, Any]:
    return {
        "bind": f"{host}:{port}",
        "workers": workers,
        "worker_class": uvicorn.workers.UvicornWorker,
        'timeout': timeout,
    }
