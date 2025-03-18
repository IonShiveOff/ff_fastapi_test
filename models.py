from pydantic import BaseModel, field_validator


class InputData(BaseModel):
    client_id: int
    iin_bin: str

    @field_validator('iin_bin')
    def iin_bin_must_be_12_digits(cls, v):
        if not (len(v) == 12 and v.isdigit()):
            raise ValueError('Invalid string: must be 12 digits long')
        return v
