# 数据库操作
from sqlalchemy.orm import Session
from app.models.image import Image
from app.schemas.image import ImageCreate

def create_image(db: Session, image: ImageCreate):
    db_image = Image(**image.dict())
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

def get_all_images(db: Session):
    return db.query(Image).all()

def delete_image_by_id(db: Session,image_id: int):
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if db_image:
        db.delete(db_image)
        db.commit()
    return db_image