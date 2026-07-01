"""
Data models for the evaluation appeal system.
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class UserRole(str, Enum):
    """User roles in the system."""
    AGENT = "agent"
    SUPERVISOR = "supervisor"


class EvaluationStatus(str, Enum):
    """Status of an evaluation."""
    PASSED = "passed"
    FAILED = "failed"
    NEEDS_IMPROVEMENT = "needs_improvement"


class AppealStatus(str, Enum):
    """Status of an appeal."""
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    MORE_INFO_REQUESTED = "more_info_requested"


class AppealPriority(str, Enum):
    """Priority level for appeals."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class User(BaseModel):
    """User model representing agents and supervisors."""
    id: str
    name: str
    email: str
    role: UserRole


class Evaluation(BaseModel):
    """Evaluation model."""
    id: str
    agent_id: str
    evaluator_id: str
    status: EvaluationStatus
    score: float = Field(ge=0, le=100)
    feedback: str
    criteria: dict
    evaluated_at: datetime
    task_description: str


class AIAppealSuggestion(BaseModel):
    """AI-generated suggestions for an appeal."""
    suggested_points: List[str]
    tone_recommendation: str
    strength_assessment: str
    additional_context_needed: List[str]
    estimated_success_probability: float = Field(ge=0, le=1)


class Appeal(BaseModel):
    """Appeal model with AI assistance."""
    id: str
    evaluation_id: str
    agent_id: str
    status: AppealStatus
    priority: AppealPriority = AppealPriority.MEDIUM
    reason: str
    supporting_evidence: List[str] = []
    ai_suggestion: Optional[AIAppealSuggestion] = None
    created_at: datetime
    updated_at: datetime
    submitted_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    supervisor_notes: Optional[str] = None
    decision_reason: Optional[str] = None


class AITriageAnalysis(BaseModel):
    """AI-powered triage analysis for supervisor."""
    appeal_id: str
    priority_recommendation: AppealPriority
    validity_score: float = Field(ge=0, le=1)
    key_points: List[str]
    red_flags: List[str]
    supporting_factors: List[str]
    recommended_action: str
    estimated_review_time_minutes: int
    similar_past_cases: List[str] = []


class SupervisorDecision(BaseModel):
    """Supervisor's decision on an appeal."""
    appeal_id: str
    supervisor_id: str
    decision: AppealStatus  # APPROVED, REJECTED, or MORE_INFO_REQUESTED
    reason: str
    action_items: List[str] = []
    decided_at: datetime
