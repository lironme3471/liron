"""
Supervisor service for triaging and deciding on appeals.
"""
from datetime import datetime
from typing import List, Optional, Dict
from collections import defaultdict

from .models import (
    Appeal,
    AppealStatus,
    AppealPriority,
    Evaluation,
    User,
    AITriageAnalysis,
    SupervisorDecision,
)
from .ai_service import AIService


class SupervisorService:
    """Service for managing appeals from the supervisor perspective."""
    
    def __init__(self, ai_service: AIService, appeals: dict):
        """
        Initialize supervisor service.
        
        Args:
            ai_service: AI service for analysis
            appeals: Shared appeals dictionary from AppealService
        """
        self.ai_service = ai_service
        self.appeals = appeals
        self.triage_analyses: Dict[str, AITriageAnalysis] = {}
        self.decisions: Dict[str, SupervisorDecision] = {}
    
    def get_pending_appeals(
        self,
        priority_filter: Optional[AppealPriority] = None,
        sort_by: str = "priority"  # priority, date, score
    ) -> List[tuple[Appeal, AITriageAnalysis]]:
        """
        Get all pending appeals with AI triage analysis.
        
        Args:
            priority_filter: Optional priority level to filter by
            sort_by: How to sort the appeals
            
        Returns:
            List of tuples (Appeal, AITriageAnalysis)
        """
        pending_appeals = [
            appeal for appeal in self.appeals.values()
            if appeal.status in [AppealStatus.SUBMITTED, AppealStatus.UNDER_REVIEW]
        ]
        
        if priority_filter:
            pending_appeals = [a for a in pending_appeals if a.priority == priority_filter]
        
        # Generate triage analysis for each appeal if not already done
        results = []
        for appeal in pending_appeals:
            if appeal.id not in self.triage_analyses:
                # In a real system, we'd fetch the evaluation from a database
                # For now, we'll create a mock evaluation
                evaluation = self._get_evaluation(appeal.evaluation_id)
                analysis = self.ai_service.analyze_appeal_for_triage(
                    appeal,
                    evaluation
                )
                self.triage_analyses[appeal.id] = analysis
            
            results.append((appeal, self.triage_analyses[appeal.id]))
        
        # Sort based on preference
        if sort_by == "priority":
            priority_order = {
                AppealPriority.URGENT: 0,
                AppealPriority.HIGH: 1,
                AppealPriority.MEDIUM: 2,
                AppealPriority.LOW: 3
            }
            results.sort(key=lambda x: (
                priority_order.get(x[1].priority_recommendation, 999),
                -x[1].validity_score
            ))
        elif sort_by == "date":
            results.sort(key=lambda x: x[0].submitted_at or x[0].created_at)
        elif sort_by == "score":
            results.sort(key=lambda x: -x[1].validity_score)
        
        return results
    
    def get_appeal_with_analysis(
        self,
        appeal_id: str,
        evaluation: Evaluation
    ) -> tuple[Appeal, AITriageAnalysis]:
        """
        Get a specific appeal with its AI analysis.
        
        Args:
            appeal_id: ID of the appeal
            evaluation: The original evaluation
            
        Returns:
            Tuple of (Appeal, AITriageAnalysis)
        """
        appeal = self.appeals.get(appeal_id)
        if not appeal:
            raise ValueError(f"Appeal {appeal_id} not found")
        
        # Generate or retrieve triage analysis
        if appeal_id not in self.triage_analyses:
            analysis = self.ai_service.analyze_appeal_for_triage(
                appeal,
                evaluation
            )
            self.triage_analyses[appeal_id] = analysis
        
        return appeal, self.triage_analyses[appeal_id]
    
    def make_decision(
        self,
        supervisor: User,
        appeal_id: str,
        decision: AppealStatus,
        reason: str,
        action_items: Optional[List[str]] = None
    ) -> SupervisorDecision:
        """
        Make a decision on an appeal.
        
        Args:
            supervisor: The supervisor making the decision
            appeal_id: ID of the appeal
            decision: APPROVED, REJECTED, or MORE_INFO_REQUESTED
            reason: Reason for the decision
            action_items: Optional list of action items
            
        Returns:
            SupervisorDecision object
        """
        appeal = self.appeals.get(appeal_id)
        if not appeal:
            raise ValueError(f"Appeal {appeal_id} not found")
        
        if decision not in [
            AppealStatus.APPROVED,
            AppealStatus.REJECTED,
            AppealStatus.MORE_INFO_REQUESTED
        ]:
            raise ValueError(f"Invalid decision status: {decision}")
        
        # Update appeal
        appeal.status = decision
        appeal.reviewed_by = supervisor.id
        appeal.reviewed_at = datetime.now()
        appeal.supervisor_notes = reason
        appeal.updated_at = datetime.now()
        
        # Create decision record
        decision_obj = SupervisorDecision(
            appeal_id=appeal_id,
            supervisor_id=supervisor.id,
            decision=decision,
            reason=reason,
            action_items=action_items or [],
            decided_at=datetime.now()
        )
        
        self.decisions[appeal_id] = decision_obj
        return decision_obj
    
    def get_decision_draft(
        self,
        appeal_id: str,
        decision_type: str
    ) -> str:
        """
        Get an AI-generated draft decision message.
        
        Args:
            appeal_id: ID of the appeal
            decision_type: 'approve', 'reject', or 'more_info'
            
        Returns:
            Draft decision message
        """
        appeal = self.appeals.get(appeal_id)
        if not appeal:
            raise ValueError(f"Appeal {appeal_id} not found")
        
        analysis = self.triage_analyses.get(appeal_id)
        if not analysis:
            # Generate analysis if not exists
            evaluation = self._get_evaluation(appeal.evaluation_id)
            analysis = self.ai_service.analyze_appeal_for_triage(appeal, evaluation)
            self.triage_analyses[appeal_id] = analysis
        
        return self.ai_service.generate_decision_draft(
            appeal,
            analysis,
            decision_type
        )
    
    def bulk_triage(
        self,
        appeal_ids: List[str],
        evaluations: Dict[str, Evaluation]
    ) -> Dict[str, AITriageAnalysis]:
        """
        Perform bulk triage on multiple appeals for efficiency.
        
        Args:
            appeal_ids: List of appeal IDs to triage
            evaluations: Dictionary of evaluation_id -> Evaluation
            
        Returns:
            Dictionary of appeal_id -> AITriageAnalysis
        """
        results = {}
        for appeal_id in appeal_ids:
            appeal = self.appeals.get(appeal_id)
            if appeal:
                evaluation = evaluations.get(appeal.evaluation_id)
                if evaluation:
                    if appeal_id not in self.triage_analyses:
                        analysis = self.ai_service.analyze_appeal_for_triage(
                            appeal,
                            evaluation
                        )
                        self.triage_analyses[appeal_id] = analysis
                    results[appeal_id] = self.triage_analyses[appeal_id]
        return results
    
    def get_summary_statistics(self) -> Dict:
        """
        Get summary statistics for the supervisor dashboard.
        
        Returns:
            Dictionary with statistics
        """
        total_appeals = len(self.appeals)
        
        status_counts = defaultdict(int)
        priority_counts = defaultdict(int)
        
        for appeal in self.appeals.values():
            status_counts[appeal.status.value] += 1
            priority_counts[appeal.priority.value] += 1
        
        pending = status_counts.get(AppealStatus.SUBMITTED.value, 0) + \
                 status_counts.get(AppealStatus.UNDER_REVIEW.value, 0)
        
        return {
            "total_appeals": total_appeals,
            "pending_appeals": pending,
            "approved": status_counts.get(AppealStatus.APPROVED.value, 0),
            "rejected": status_counts.get(AppealStatus.REJECTED.value, 0),
            "status_breakdown": dict(status_counts),
            "priority_breakdown": dict(priority_counts),
            "avg_review_time_estimate": sum(
                a.estimated_review_time_minutes 
                for a in self.triage_analyses.values()
            ) / max(len(self.triage_analyses), 1)
        }
    
    def _get_evaluation(self, evaluation_id: str) -> Evaluation:
        """
        Mock method to get evaluation by ID.
        In production, this would fetch from a database.
        """
        # This is a mock implementation
        return Evaluation(
            id=evaluation_id,
            agent_id="agent_123",
            evaluator_id="eval_456",
            status="failed",
            score=55.0,
            feedback="Performance did not meet expectations in several key areas.",
            criteria={"quality": 50, "timeliness": 60, "communication": 55},
            evaluated_at=datetime.now(),
            task_description="Customer service call handling evaluation"
        )
