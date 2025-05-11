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
import shutil
from idlelib.iomenu import encoding

from typing import Optional
import router
from fastapi import FastAPI, File, UploadFile, HTTPException, Depends,Response
from sqlalchemy.orm import Session
from app.models.image import Image, Base, engine
from app.schemas.image import ImageCreate, ImageResponse
from app.crud.image import create_image, get_all_images, delete_image_by_id
from app.utils.config import settings, reload_settings
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

## 保存图片
async def save_image(file: UploadFile, save_dir: Path) -> dict:
    """保存图片并返回存储信息（包含自动重命名）"""
    # 校验文件类型（简单校验MIME类型，可增强内容校验）
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="仅支持图片文件")

    # 生成唯一文件名
    unique_filename = generate_unique_filename(file.filename)
    save_path = save_dir / unique_filename

    # 写入文件
    try:
        with open(save_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(500, detail=f"文件保存失败: {str(e)}")

    # 返回存储信息（包含URL）
    url = f"http://{settings.server_host}:{settings.server_port}/{save_dir.name}/{unique_filename}"
    return {
        "filename": unique_filename,  # 存储唯一文件名（避免数据库唯一约束冲突）
        "save_path": str(save_path),
        "url": url
    }

## 保存自定义图片
async def save_customimage(file: UploadFile, save_dir: Path) -> str:
    """保存图片并返回保存路径（字符串）"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, detail="仅支持图片文件")

    unique_filename = generate_unique_filename(file.filename)
    save_path = save_dir / unique_filename

    try:
        with open(save_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(500, detail=f"文件保存失败: {str(e)}")

    # 返回相对路径（../img/文件名）
    return f"../img/{unique_filename}"


##更新.env中的CUSTOM_UPLOAD_PATH
def update_custom_upload_path(new_path: str, env_file: Optional[str] = None) -> None:
    ## 验证新路径是否有效
    if not new_path.strip():
        raise ValueError("新路径不能为空")

    ## 确定.env文件路径
    if not env_file:
        project_root = Path(__file__).parent.parent
        env_file = project_root / ".env"

    ## 创建备份
    shutil.copy2(env_file, f"{env_file}.bak")

    ## 读取并更新.env文件内容
    updated = False
    new_lines = []

    with open(env_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for line in lines:
        # 处理注释或空行
        if line.strip().startswith("#")or not line.strip():
            new_lines.append(line)
            continue
        # 查找CUSTOM_UPLOAD_PATH配置项
        if line.strip().lower().startswith("custom_upload_path"):
            # 更新配置项
            key_part = line.split("=", 1)[0]
            new_lines.append(f"{key_part}={new_path.strip()}\n")
            updated = True
        else:
            #保留其他配置项
            new_lines.append(line)
    ## 如果原文件中没有CUSTOM_UPLOAD_PATH配置项，则将其添加到文件末尾
    if not updated:
        new_lines.append(f"\nCUSTOM_UPLOAD_PATH={new_path.strip()}\n")

    ## 写回更新后的内容
    with open(env_file, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    print(f"已成功更新 CUSTOM_UPLOAD_PATH 为:{new_path.strip()}")


## 普通上传
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


## 自定义上传图片的路径
@app.post("/update-upload-path")
async def update_upload_path(new_path: str):
    try:
        update_custom_upload_path(new_path)
        reload_settings()
        return {"message": f"上传路径已更新为: {new_path}"}
    except ValueError as e:
        raise HTTPException(400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(404, detail=str(e))
    except Exception as e:
        raise HTTPException(500, detail=f"服务器内部错误: {str(e)}")





## 根据自定义路径上传图片
# @app.post("/upload/custom/", response_model=ImageResponse)
# async def upload_image_to_custom_path(file: UploadFile = File(...), db: Session = Depends(get_db)):
#     # 打印当前配置值，验证是否更新
#     print(f"当前自定义上传路径: {settings.custom_upload_path}")
#
#     if not settings.custom_upload_path:
#         raise HTTPException(400, detail="未配置自定义上传路径")
#
#     custom_dir = Path(settings.custom_upload_path)
#     os.makedirs(custom_dir, exist_ok=True)
#
#     # 打印实际创建的目录路径
#     print(f"创建目录: {custom_dir.absolute()}")
#
#     storage_info = await save_customimage(file, custom_dir)
#     db_image = create_image(db, ImageCreate(**storage_info))
#     return db_image

# 自定义路径上传路由
@app.post("/upload/custom/")
async def upload_image_to_custom_path(file: UploadFile = File(...)):
    if not settings.custom_upload_path:
        raise HTTPException(400, detail="未配置自定义上传路径")

    custom_dir = Path(settings.custom_upload_path)
    os.makedirs(custom_dir, exist_ok=True)

    save_path = await save_customimage(file, custom_dir)



    # 返回纯文本响应，避免 JSON 序列化
    return Response(content=save_path, media_type="text/plain")
