from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()

class AIAnalysis(Base):
    __tablename__ = "ai_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    realism_score = Column(Integer)
    recommended_price = Column(Integer)
    time_estimate = Column(Integer)
    risks_detected = Column(ARRAY(String))
    used_model = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)  # <- BIGINT для больших Telegram ID
    username = Column(String(100))
    full_name = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))  # можно BigInteger, если много клиентов
    
    # Квалификация
    project_type = Column(String(50))  # "Лонгрид для YouTube", "Подкаст/интервью", etc
    duration_raw = Column(String(50))   # Исходный материал
    duration_final = Column(String(50)) # Готовое видео
    services = Column(ARRAY(String))    # Выбранные услуги
    deadline = Column(String(50))       # Срок сдачи
    budget = Column(String(50))         # Бюджет
    
    # Техническая информация
    source_links = Column(Text)
    style_examples = Column(Text)
    additional_notes = Column(Text)
    
    # Статус
    status = Column(String(20), default="new")  # new, in_progress, completed, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
