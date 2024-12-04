from fastapi import APIRouter, HTTPException
from models import UserCreateRequest, UserResponse, BirthdayRequest
from typing import Dict
from exceptions import InvalidItemIdException
from datetime import datetime


router = APIRouter()


def calculate_days_until_next_birthday(birthdate: str) -> int:
    birth_date = datetime.strptime(birthdate, "%Y-%m-%d").date()

    today = datetime.today().date()
    next_birthday = birth_date.replace(year=today.year)

    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)

    delta = next_birthday - today
    return delta.days

@router.post("/birthday")
def calculate_birthday(request: BirthdayRequest):
    try:
        days_left = calculate_days_until_next_birthday(request.birthdate)
        return {"message": f"Hello {request.name}, your next birthday is in {days_left} days!"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid birthdate format. Please use 'YYYY-MM-DD' {e}")


items_db: Dict[int, str] = {
    1: "Item A",
    2: "Item B",
    3: "Item C"
}


def validate_item_id(item_id: int):
    if not isinstance(item_id, int) or item_id <= 0:
        raise InvalidItemIdException(item_id)


@router.get("/item/{item_id}")
def get_item(item_id: int):
    validate_item_id(item_id)
    item = items_db.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "item_name": item}


@router.delete("/item/{item_id}")
def delete_item(item_id: int):
    validate_item_id(item_id)
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return {"message": f"Item {item_id} deleted successfully"}


@router.get("/")
def read_root():
    return {"message": "Bem-vindo FastAPI!"}


@router.get("/status")
def get_status():
    return {"status": "Servidor funcionando!"}


@router.get("/user/{username}", response_model=UserResponse)
def greet_user(username: str):
    valid_users = ["john", "alice", "bob"]

    if username not in valid_users:
        raise HTTPException(status_code=404, detail="User not found")

    return {"username": username, "message": f"Welcome, {username}!"}

@router.post("/create-user", response_model=UserCreateRequest)
def create_user(user: UserCreateRequest):
    return user
