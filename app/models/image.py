# app/models/image.py（最简正确模型）
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()
DATABASE_URL = "sqlite:///./picbed.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, autoincrement=True)  # 唯一主键，自增
    filename = Column(String(255), unique=True, nullable=False)  # 添加长度限制（非必需，但推荐）
    save_path = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    upload_time = Column(DateTime, default=datetime.now, nullable=False)