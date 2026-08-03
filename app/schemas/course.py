from pydantic import BaseModel, ConfigDict, Field


class CourseCreate(BaseModel):
    code: str = Field(min_length=2, max_length=20, examples=["CS204"])
    title: str = Field(min_length=2, max_length=160, examples=["Data Structures"])
    description: str | None = None


class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    title: str
    description: str | None
    material_count: int = 0