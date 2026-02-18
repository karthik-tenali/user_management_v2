import uuid
from datetime import date, datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, text, ForeignKey, Date, Integer
from sqlalchemy.dialects.postgresql import UUID
from app.db.session import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    title: Mapped[str] = mapped_column(String(300), index=True, nullable=False)
    author: Mapped[str] = mapped_column(String(150), index=True, nullable=False)
    
    publisher: Mapped[str | None] = mapped_column(String(200), nullable=True)
    published_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    page_count: Mapped[int | None] = mapped_column(Integer, nullable=True)


    owner_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.uid"),
        nullable=True,   
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )   

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    owner: Mapped["User"] = relationship(back_populates="books") # type: ignore
