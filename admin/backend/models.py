"""
Реэкспорт моделей из app.database.models для обратной совместимости
Все модели теперь находятся в app.database.models
"""
from app.database.models import Base, Client, Project, AIAnalysis

__all__ = ["Base", "Client", "Project", "AIAnalysis"]
