from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.image import Image, Base, engine
from app.schemas.image import ImageCreate, ImageResponse
from app.crud.image import create_image, get_all_images, delete_image_by_id
from app.utils.storage import save_image
from app.dependencies import get_db

app = FastAPI(title="GDYL图床", version="1.0.0")

Base.metadata.create_all(bind=engine)


@app.post("/upload/",response_model=ImageResponse)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="仅支持图片文件")
    storage_info = await  save_image(file)
    db_image = create_image(db, ImageCreate(**storage_info))
    return db_image

@app.get("/images/", response_model=list[ImageResponse])
def get_image_list(db: Session = Depends(get_db)):
    return get_all_images(db)

@app.delete("/images/{image_id}")
def delete_image(image_id: int, db: Session = Depends(get_db)):
    db_image = delete_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(404, detail="图片不存在")
    import os
    os.remove(db_image.save_path)
    return {"message": "删除成功"}