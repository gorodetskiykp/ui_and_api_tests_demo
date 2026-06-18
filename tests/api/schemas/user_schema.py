
from pydantic import BaseModel, Field, HttpUrl


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")
    job: str = Field(..., min_length=1, max_length=100, description="Должность")


class UserUpdate(UserCreate):
    pass


class UserResponse(BaseModel):
    name: str
    job: str
    id: str | None = None
    createdAt: str | None = None
    updatedAt: str | None = None


class UserData(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    avatar: HttpUrl


class SupportInfo(BaseModel):
    url: HttpUrl
    text: str


class UserListResponse(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[UserData]
    support: SupportInfo


class SingleUserResponse(BaseModel):
    data: UserData
    support: SupportInfo
