from fastapi import APIRouter

from src.users.schemas import CreateUser
from src.users import crud

router = APIRouter()


@router.get("/")
async def get_users():
    return {"TODO": "return all users"}


@router.get("/{user_id}/")
async def get_users(user_id: int):
    return {"user_id": user_id}


@router.post("/")
async def create_user(user: CreateUser):
    return crud.create_user(user)
