from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Имя пользователя")
    job: str = Field(..., min_length=1, max_length=100, description="Должность")


class UserUpdate(UserCreate):
    pass


class UserResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    job: str
    id: str | None = None
    created_at: str | None = Field(default=None, alias="createdAt")
    updated_at: str | None = Field(default=None, alias="updatedAt")


class UserData(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    email: str
    first_name: str = Field(alias="first_name")
    last_name: str = Field(alias="last_name")
    avatar: HttpUrl


class SupportInfo(BaseModel):
    url: HttpUrl
    text: str


class UserListResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    page: int
    per_page: int
    total: int
    total_pages: int
    data: list[UserData]
    support: SupportInfo


class SingleUserResponse(BaseModel):
    data: UserData
    support: SupportInfo
