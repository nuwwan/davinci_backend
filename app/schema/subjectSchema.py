from pydantic import BaseModel


class SubjectBase(BaseModel):
    name: str
    description: str | None = None


class SubjectCreate(SubjectBase):
    pass


class SubjectResponse(SubjectBase):
    id: int

    class Config:
        from_attributes = True
