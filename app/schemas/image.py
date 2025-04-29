# 请求/响应数据结构
from pydantic import BaseModel
from datetime import  datetime

class ImageCreate(BaseModel):
    filename: str
    save_path: str
    url: str

class ImageResponse(ImageCreate):
    id: int
    upload_time: datetime

    class Config:
        from_attributes = True