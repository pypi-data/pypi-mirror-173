from typing import Literal

from pydantic import BaseModel


class Ack(BaseModel):
    AckMessageID: str
    TypeName: Literal["gridworks.ack"] = "gridworks.ack"
