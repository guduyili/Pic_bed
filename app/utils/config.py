# 配置管理
import os

# 可以在这里添加更多配置项，例如数据库连接信息、存储目录等
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./picbed.db")
STORAGE_DIR = os.getenv("STORAGE_DIR", "static/images")