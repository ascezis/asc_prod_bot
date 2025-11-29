from sqlalchemy import Column, Integer, BigInteger, String, Text, ForeignKey, ARRAY, DateTime, func
from .database import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    username = Column(String(100))
    full_name = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    project_type = Column(String(50))
    duration_raw = Column(String(50))
    duration_final = Column(String(50))
    services = Column(ARRAY(String))
    deadline = Column(String(50))
    budget = Column(String(50))
    source_links = Column(Text)
    style_examples = Column(Text)
    additional_notes = Column(Text)
    status = Column(String(20), default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class AIAnalysis(Base):
    __tablename__ = "ai_analyses"
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    realism_score = Column(Integer)
    recommended_price = Column(Integer)
    time_estimate = Column(Integer)
    risks_detected = Column(ARRAY(String))
    used_model = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
