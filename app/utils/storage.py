import uuid
from fastapi import UploadFile
from pathlib import Path
from .config import settings

# 获取存储目录
STORAGE_DIR = Path(settings.storage_dir)
# 创建存储目录（如果不存在）
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# async def save_image(file: UploadFile):
#     """保存文件到本地并返回存储信息"""
#     try:
#         # 提取文件扩展名
#         file_ext = file.filename.split(".")[-1]
#         # 生成唯一的保存文件名
#         save_filename = f"{str(uuid.uuid4())}.{file_ext}"
#         # 构建完整的保存路径
#         save_path = STORAGE_DIR / save_filename
#
#         # 异步读取上传文件的内容
#         content = await file.read()
#         # 以二进制写入模式打开文件并写入内容
#         with open(save_path, "wb") as f:
#             f.write(content)
#
#         return {
#             "filename": file.filename,
#             "save_path": str(save_path),
#             "url": f"http://localhost:8000/static/images/{save_filename}"
#         }
#     except Exception as e:
#         # 处理保存文件时可能出现的异常
#         raise ValueError(f"保存文件时出错: {e}")

async def save_image(file: UploadFile):
    """保存文件到本地并返回存储信息（使用环境变量配置的目录）"""
    file_ext = file.filename.split(".")[-1]
    save_filename = f"{str(uuid.uuid4())}.{file_ext}"
    save_path = STORAGE_DIR / save_filename

    with open(save_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 生成完整访问URL 使用配置的host和port
    url = f"http://{settings.server_host}:{settings.server_port}/static/images/{save_filename}"

    return{
        "filename": save_filename,
        "save_path": str(save_path),
        "url": url
    }