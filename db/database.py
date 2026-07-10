from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://pytch_db_0ygw_user:4H2AiJ4EzfbKzf86BFfouMNQdHlnKIpM@dpg-d9bk386cjfls738id570-a.frankfurt-postgres.render.com/pytch_db_0ygw"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    pass
    # if not engine.dialect(engine, "users"):
        # Base.metadata.create_all(engine)