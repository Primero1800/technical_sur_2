from fastapi import APIRouter

from src.users.schemas import CreateUser
from src.users import crud

router = APIRouter()


@router.get("/users/")
async def get_users():
    return {"TODO": "return all users"}


@router.get("/users/{user_id}/")
async def get_users(user_id: int):
    return {"user_id": user_id}


@router.post("/users/")
async def create_user(user: CreateUser):
    return crud.create_user(user)
