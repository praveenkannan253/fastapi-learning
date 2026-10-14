from pydantic import BaseModel,EmailStr


class User(BaseModel):
    name: str
    age: int
    email: EmailStr


valid_data = User(name="Praveen", age="22", email="virat@gmail.com")
print(valid_data)
