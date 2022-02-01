from pydantic import BaseModel, constr, EmailStr, PastDate


class UserRegistration(BaseModel):
    username: constr(max_length=255)
    email: EmailStr
    password: constr(max_length=100)
    first_name: constr(max_length=100)
    last_name: constr(max_length=100)
    birth_date: PastDate