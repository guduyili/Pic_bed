# 依赖注入
from sqlalchemy.orm import Session
from app.models.image import engine


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()