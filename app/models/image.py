# 数据库模型
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
DATABASE_URL = "sqlite:///./picbed.db"
engin = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)  # 原始文件名
    save_path = Column(Integer, primary_key=True, index=True)  # 存储路径
    url = Column(String, index=True)  # 访问链接
    upload_time = Column(DateTime, default=datetime.now())
