from pydantic import BaseModel


class InputData(BaseModel):
    data: dict