import atexit
import datetime
import os

from sqlalchemy import DateTime, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "Essketit")
POSTGRES_USER = os.getenv("POSTGRES_USER", "lilpump")
POSTGRES_DB = os.getenv("POSTGRES_DB", "gucci")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")


PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    header: Mapped[str] = mapped_column(
        String(100), unique=True, index=True, nullable=False
    )
    description: Mapped[str] = mapped_column(String(2048), index=True, nullable=True)
    creation_date: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    owner: Mapped[str] = mapped_column(String(100), index=True, nullable=False)

    @property
    def dict(self):
        return {
            "id": self.id,
            "header": self.header,
            "description": self.description,
            "creation_date": self.creation_date.isoformat(),
            "owner": self.owner,
        }


Base.metadata.create_all(bind=engine)
