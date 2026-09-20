from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

def now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__="users"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    username:Mapped[str]=mapped_column(String(80),unique=True,index=True)
    password_hash:Mapped[str]=mapped_column(String(255))
    role:Mapped[str]=mapped_column(String(30),default="analyst")
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)

class Case(Base):
    __tablename__="cases"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    case_number:Mapped[str]=mapped_column(String(80),unique=True,index=True)
    title:Mapped[str]=mapped_column(String(200))
    description:Mapped[str]=mapped_column(Text,default="")
    status:Mapped[str]=mapped_column(String(30),default="open")
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    evidence:Mapped[list["Evidence"]]=relationship(back_populates="case",cascade="all, delete-orphan")

class Evidence(Base):
    __tablename__="evidence"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    case_id:Mapped[int]=mapped_column(ForeignKey("cases.id"),index=True)
    name:Mapped[str]=mapped_column(String(255))
    path:Mapped[str]=mapped_column(String(500))
    sha256:Mapped[str]=mapped_column(String(64),index=True)
    size_bytes:Mapped[int]=mapped_column(Integer)
    collected_by:Mapped[str]=mapped_column(String(80))
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
    case:Mapped[Case]=relationship(back_populates="evidence")

class AuditLog(Base):
    __tablename__="audit_logs"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    username:Mapped[str]=mapped_column(String(80))
    action:Mapped[str]=mapped_column(String(120))
    target:Mapped[str]=mapped_column(String(255),default="")
    created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
