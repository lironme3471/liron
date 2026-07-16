"""
Evaluation Appeal System with AI Assistance.

A system for agents to appeal evaluations with AI-powered suggestions,
and for supervisors to efficiently triage and decide on appeals.
"""

from .models import (
    User,
    UserRole,
    Evaluation,
    EvaluationStatus,
    Appeal,
    AppealStatus,
    AppealPriority,
    AIAppealSuggestion,
    AITriageAnalysis,
    SupervisorDecision,
)
from .ai_service import AIService
from .appeal_service import AppealService
from .supervisor_service import SupervisorService

__version__ = "1.0.0"

__all__ = [
    "User",
    "UserRole",
    "Evaluation",
    "EvaluationStatus",
    "Appeal",
    "AppealStatus",
    "AppealPriority",
    "AIAppealSuggestion",
    "AITriageAnalysis",
    "SupervisorDecision",
    "AIService",
    "AppealService",
    "SupervisorService",
]
