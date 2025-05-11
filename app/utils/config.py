# import os
# from pydantic_settings import BaseSettings, SettingsConfigDict
#
# class Settings(BaseSettings):
#     """应用配置类，从.env文件或环境变量加载配置"""
#     # 数据库连接 URL，默认使用 SQLite
#     database_url: str = os.getenv("DATABASE_URL", "sqlite:///./picbed.db")
#     # 图片存储目录，默认是 static/images
#     storage_dir: str = os.getenv("STORAGE_DIR", "static/images")
#
#     server_host: str = os.getenv("SERVER_HOST", "127.0.0.1")
#     server_port: int = int(os.getenv("SERVER_PORT", "8000"))
#
#     # 自定义上传路径
#     custom_upload_path: str = os.getenv("CUSTOM_UPLOAD_PATH", "")
#
#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         case_sensitive=False
#     )
#
# # 创建 Settings 实例
# settings = Settings()

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """应用配置类，从.env文件或环境变量加载配置"""
    # 数据库连接 URL，默认使用 SQLite
    database_url: str = "sqlite:///./picbed.db"
    # 图片存储目录，默认是 static/images
    storage_dir: str = "static/images"
    # 服务器配置
    server_host: str = "127.0.0.1"
    server_port: int = 8000
    # 自定义上传路径
    custom_upload_path: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False  # 修正拼写错误
    )



# 创建 Settings 实例
settings = Settings()

def reload_settings():
    """重新加载配置"""
    global settings
    settings = Settings()
    return settings