"""
Appeal service for agent-side functionality.
"""
from datetime import datetime
from typing import List, Optional
import uuid

from .models import (
    Appeal,
    AppealStatus,
    AppealPriority,
    Evaluation,
    User,
    AIAppealSuggestion,
)
from .ai_service import AIService


class AppealService:
    """Service for managing appeals from the agent perspective."""
    
    def __init__(self, ai_service: AIService):
        """Initialize appeal service with AI service."""
        self.ai_service = ai_service
        self.appeals: dict[str, Appeal] = {}
    
    def create_appeal_draft(
        self,
        agent: User,
        evaluation: Evaluation,
        initial_thoughts: str = ""
    ) -> tuple[Appeal, AIAppealSuggestion]:
        """
        Create a draft appeal with AI assistance.
        
        Args:
            agent: The agent creating the appeal
            evaluation: The evaluation being appealed
            initial_thoughts: Agent's initial thoughts on why they're appealing
            
        Returns:
            Tuple of (Appeal, AIAppealSuggestion)
        """
        # Generate AI suggestions
        ai_suggestion = self.ai_service.generate_appeal_suggestions(
            evaluation,
            initial_thoughts
        )
        
        # Create draft appeal
        appeal = Appeal(
            id=str(uuid.uuid4()),
            evaluation_id=evaluation.id,
            agent_id=agent.id,
            status=AppealStatus.DRAFT,
            priority=AppealPriority.MEDIUM,
            reason=initial_thoughts,
            supporting_evidence=[],
            ai_suggestion=ai_suggestion,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.appeals[appeal.id] = appeal
        return appeal, ai_suggestion
    
    def update_appeal_draft(
        self,
        appeal_id: str,
        reason: Optional[str] = None,
        supporting_evidence: Optional[List[str]] = None,
        priority: Optional[AppealPriority] = None
    ) -> Appeal:
        """
        Update a draft appeal.
        
        Args:
            appeal_id: ID of the appeal to update
            reason: Updated reason for appeal
            supporting_evidence: Updated supporting evidence
            priority: Updated priority
            
        Returns:
            Updated appeal
        """
        appeal = self.appeals.get(appeal_id)
        if not appeal:
            raise ValueError(f"Appeal {appeal_id} not found")
        
        if appeal.status != AppealStatus.DRAFT:
            raise ValueError(f"Appeal {appeal_id} is not in draft status")
        
        if reason is not None:
            appeal.reason = reason
        if supporting_evidence is not None:
            appeal.supporting_evidence = supporting_evidence
        if priority is not None:
            appeal.priority = priority
        
        appeal.updated_at = datetime.now()
        return appeal
    
    def submit_appeal(self, appeal_id: str) -> Appeal:
        """
        Submit a draft appeal for review.
        
        Args:
            appeal_id: ID of the appeal to submit
            
        Returns:
            Submitted appeal
        """
        appeal = self.appeals.get(appeal_id)
        if not appeal:
            raise ValueError(f"Appeal {appeal_id} not found")
        
        if appeal.status != AppealStatus.DRAFT:
            raise ValueError(f"Appeal {appeal_id} is not in draft status")
        
        if not appeal.reason or len(appeal.reason) < 20:
            raise ValueError("Appeal reason must be at least 20 characters")
        
        appeal.status = AppealStatus.SUBMITTED
        appeal.submitted_at = datetime.now()
        appeal.updated_at = datetime.now()
        
        return appeal
    
    def get_appeal_status(self, appeal_id: str) -> Appeal:
        """
        Get the current status of an appeal.
        
        Args:
            appeal_id: ID of the appeal
            
        Returns:
            Appeal object
        """
        appeal = self.appeals.get(appeal_id)
        if not appeal:
            raise ValueError(f"Appeal {appeal_id} not found")
        return appeal
    
    def list_agent_appeals(
        self,
        agent_id: str,
        status_filter: Optional[AppealStatus] = None
    ) -> List[Appeal]:
        """
        List all appeals for a specific agent.
        
        Args:
            agent_id: ID of the agent
            status_filter: Optional status to filter by
            
        Returns:
            List of appeals
        """
        appeals = [
            appeal for appeal in self.appeals.values()
            if appeal.agent_id == agent_id
        ]
        
        if status_filter:
            appeals = [a for a in appeals if a.status == status_filter]
        
        return sorted(appeals, key=lambda a: a.created_at, reverse=True)
