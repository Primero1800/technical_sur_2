from functools import partial
from typing import Any, List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


router = APIRouter(prefix='/temp')


class GetDataFromHeader:
    def __init__(
        self,
        param_names: List[str] = ['data',],
        get_all: bool = False
    ):
        self.param_names = param_names.copy()
        self.get_all = get_all

    def __call__(self, request: Request) -> dict:
        result = {}
        for param in self.param_names:
            if param not in request.headers:
                if self.get_all:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"No {param} in request"
                    )
                else:
                    continue
            result[param] = request.headers[param]
        return result


@router.get("/head")
# @router.get("head/{id}")
async def temp(
        data: dict | None = Depends(
            GetDataFromHeader(['value', 's'], False)
        )):
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No valid data in request"
        )
    return data


@router.get("")
@router.get("/{id}")
async def temp(id: int):
    try:
        return {
            "id": id
        }
    except TypeError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )