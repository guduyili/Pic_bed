# from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
# from sqlalchemy.orm import Session
# from app.models.image import Image, Base, engine
# from app.schemas.image import ImageCreate, ImageResponse
# from app.crud.image import create_image, get_all_images, delete_image_by_id
# from app.utils.storage import save_image
# from app.dependencies import get_db
#
# app = FastAPI(title="GDYL图床", version="1.0.0")
#
# Base.metadata.create_all(bind=engine)
#
#
# @app.post("/upload/",response_model=ImageResponse)
# async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     if not file.content_type.startswith("image/"):
#         raise HTTPException(400, detail="仅支持图片文件")
#     storage_info = await  save_image(file)
#     db_image = create_image(db, ImageCreate(**storage_info))
#     return db_image
#
# @app.get("/images/", response_model=list[ImageResponse])
# def get_image_list(db: Session = Depends(get_db)):
#     return get_all_images(db)
#
# @app.delete("/images/{image_id}")
# def delete_image(image_id: int, db: Session = Depends(get_db)):
#     db_image = delete_image_by_id(db, image_id)
#     if not db_image:
#         raise HTTPException(404, detail="图片不存在")
#     import os
#     os.remove(db_image.save_path)
#     return {"message": "删除成功"}
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.image import Image, Base, engine
from app.schemas.image import ImageCreate, ImageResponse
from app.crud.image import create_image, get_all_images, delete_image_by_id
from app.utils.storage import save_image  # 需确保此函数包含自动重命名逻辑
from app.dependencies import get_db
import uuid
import os
from pathlib import Path

app = FastAPI(title="GDYL图床", version="1.0.0")

# 创建数据库表（仅开发环境使用，生产环境建议用Alembic迁移）
Base.metadata.create_all(bind=engine)

# 定义图片存储目录（建议从配置文件或环境变量获取）
IMAGE_STORAGE_DIR = Path(__file__).parent.parent / "static" / "images"
os.makedirs(IMAGE_STORAGE_DIR, exist_ok=True)


def generate_unique_filename(original_filename: str) -> str:
    """生成唯一文件名（UUID+原始扩展名）"""
    ext = original_filename.split(".")[-1].lower()  # 提取扩展名
    unique_id = uuid.uuid4().hex  # 生成32位UUID
    return f"{unique_id}.{ext}"


async def save_image(file: UploadFile) -> dict:
    """保存图片并返回存储信息（包含自动重命名）"""
    # 校验文件类型（简单校验MIME类型，可增强内容校验）
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="仅支持图片文件")

    # 生成唯一文件名
    unique_filename = generate_unique_filename(file.filename)
    save_path = IMAGE_STORAGE_DIR / unique_filename

    # 写入文件
    try:
        with open(save_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(500, detail=f"文件保存失败: {str(e)}")

    # 返回存储信息（包含URL，假设静态文件路由为/static/images/）
    return {
        "filename": unique_filename,  # 存储唯一文件名（避免数据库唯一约束冲突）
        "save_path": str(save_path),
        "url": f"http://localhost:8000/static/images/{unique_filename}"
    }


@app.post("/upload/", response_model=ImageResponse)
async def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db)):
    storage_info = await save_image(file)
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

    # 删除本地文件
    if os.path.exists(db_image.save_path):
        os.remove(db_image.save_path)

    return {"message": "删除成功"}