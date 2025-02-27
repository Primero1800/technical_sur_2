from fastapi import APIRouter, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


router = APIRouter(prefix='/temp')


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
