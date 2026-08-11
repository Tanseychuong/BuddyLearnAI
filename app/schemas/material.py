from pydantic import BaseModel, ConfigDict


class MaterialRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    course_id: int
    filename: str
    content_type: str | None
    status: str
    