from sqlalchemy import Column, Integer, BigInteger, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import ARRAY
import enum

Base = declarative_base()


class UserRole(str, enum.Enum):
    """Роли пользователей"""
    USER = "user"      # Заказчик - может просматривать свою информацию
    ADMIN = "admin"    # Администратор - доступ в админку
    OWNER = "owner"    # Владелец - управление модулями и полный доступ

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


class User(Base):
    """Пользователи системы (для админ-панели)"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    email = Column(String(200), unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default=UserRole.USER.value, nullable=False)  # Используем String вместо Enum для совместимости
    telegram_id = Column(BigInteger, unique=True, index=True, nullable=True)  # Связь с Telegram (опционально)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, index=True)  # <- BIGINT для больших Telegram ID
    username = Column(String(100))
    full_name = Column(String(200))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Связь с User (если зарегистрирован в админке)
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
