from pydantic import BaseModel, constr, conint


class BirthdayRequest(BaseModel):
    name: str
    birthdate: str

class UserResponse(BaseModel):
    username: str
    message: str

class UserCreateRequest(BaseModel):
    username: constr(min_length=1)
    age: conint(ge=1)
