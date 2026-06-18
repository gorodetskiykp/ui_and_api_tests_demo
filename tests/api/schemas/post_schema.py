from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок поста")
    body: str = Field(..., min_length=1, description="Текст поста")
    user_id: int = Field(..., gt=0, description="ID пользователя")


class PostUpdate(PostCreate):
    pass


class PostResponse(CamelModel):
    id: int
    title: str
    body: str
    user_id: int


class PostListItem(CamelModel):
    user_id: int
    id: int
    title: str
    body: str


class Comment(CamelModel):
    post_id: int
    id: int
    name: str
    email: str
    body: str
