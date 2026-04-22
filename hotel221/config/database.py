from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from hotel221.config.settings import settings

# Moteur SQLAlchemy connecté à PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    echo=(settings.ENV == "development"),  # log SQL en dev
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


# Dépendance FastAPI : fournit une session par requête
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
