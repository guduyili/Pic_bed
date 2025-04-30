import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """应用配置类，从.env文件或环境变量加载配置"""
    # 数据库连接 URL，默认使用 SQLite
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./picbed.db")
    # 图片存储目录，默认是 static/images
    storage_dir: str = os.getenv("STORAGE_DIR", "static/images")

    server_host: str = os.getenv("SERVER_HOST", "127.0.0.1")
    server_port: int = int(os.getenv("SERVER_PORT", "8000"))

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_senstive=False
    )

# 创建 Settings 实例
settings = Settings()