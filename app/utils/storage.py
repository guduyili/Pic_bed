# 文件存储逻辑
import os
import uuid

from fastapi import  UploadFile
from pathlib import Path

#配置默认存贮路径（可通过环境变量修改）
# 获取当前文件所在目录的上两级目录，然后拼接 "static" 和 "images" 形成存储目录路径
STORAGE_DIR = Path(__file__).parent.parent / "static" / "images"
# 创建存储目录，exist_ok防止存在报错
os.makedirs(STORAGE_DIR, exist_ok=True)

# url
url = "http://localhost:8000/static/images"

# 异步函数 上传与返回存储信息
async def save_image(file: UploadFile):
    """保存文件到本地并返回存储信息"""
    # 使用 split(".") 方法将文件名按点分割成列表，取最后一个元素即为扩展名
    file_ext = file.filename.split(".")[-1]
    # 生成一个唯一的保存文件名
    # 使用 uuid.uuid4() 生成一个随机的 UUID 将其转换为字符串后与文件扩展名拼接
    save_filename = f"{str(uuid.uuid4())}.{file_ext}"
    # 构建文件保存的完整路径
    # 将存储目录路径与保存文件名拼接
    save_path = STORAGE_DIR / save_filename
    # 以二进制写入模式打开保存文件的路径
    with open(save_path, "wb") as f:
        # 异步读取上传文件的内容
        content = await file.read()
        # 将读取到的内容写入到保存文件中
        f.write(content)

    return{
        "filename": file.filename,
        "save_path": str(save_path),
         "url": f"http://localhost:8000/static/images/{save_filename}"
    }