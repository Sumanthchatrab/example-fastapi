from typing import Optional
from pydantic import BaseModel

class config(BaseModel):
    Add_RDD_Days: str
    GC_Threshold: str 

class orderdata(BaseModel):
    OrderLine: list
    PK: str  

class body(BaseModel):
    Messages: Optional[str] = None
    Order: orderdata
    ConfigStoreMap: config















class extend(BaseModel):
    O4UPC: Optional[int] = None

class line(BaseModel):
    RequiredDeliveryDate: str
    ItemId: str
    OrderLineId: str
    Extended: extend

class respost(BaseModel):
    OrderId: str
    PK: str
    OrderLine: list
    class Config:
        orm_mode = True

