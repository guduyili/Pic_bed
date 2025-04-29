# GDYL 图床

这是一个基于 FastAPI 实现的简单图床项目，支持图片上传、查看和删除功能。

## 项目结构
- `app/`：应用核心代码
  - `models/`：数据库模型
  - `schemas/`：请求/响应数据结构
  - `crud/`：数据库操作
  - `utils/`：工具函数
  - `main.py`：FastAPI 主入口
  - `dependencies.py`：依赖注入
- `static/`：图片存储目录
- `tests/`：测试用例
- `.env`：环境变量配置（可选）
- `README.md`：项目说明文档
- `requirements.txt`：依赖列表

## 安装依赖pip install -r requirements.txt
## 启动服务uvicorn app.main:app --reload
## 使用方法
- **上传图片**：通过 `POST /upload/` 接口上传图片
- **查看图片列表**：通过 `GET /images/` 接口查看所有图片
- **删除图片**：通过 `DELETE /images/{image_id}` 接口删除指定图片
    