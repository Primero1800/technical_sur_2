from functools import partial
from typing import Any, List, Annotated, Optional

from fastapi import APIRouter, HTTPException, Depends, Body, Form
from fastapi.exceptions import RequestValidationError
from pydantic import EmailStr, BaseModel, Field
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


class User(BaseModel):
    name: Optional[str] = Field(min_length=3, max_length=30, default='John Doe')
    email: Annotated[EmailStr, Field(title='Email address', description='Valid email address of person, please')]

@router.post("/email")
# @router.post("/email/{email}")
async def temp(user: User):
    return {
        'success': True,
        **user.model_dump()
    }



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


