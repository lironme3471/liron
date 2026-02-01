"""
AI service for generating appeal suggestions and triage analysis.
This is a mock implementation that simulates AI assistance.
In production, this would integrate with OpenAI or similar services.
"""
from typing import List, Optional
import json
from datetime import datetime

from .models import (
    AIAppealSuggestion,
    AITriageAnalysis,
    Evaluation,
    Appeal,
    AppealPriority,
)


class AIService:
    """Service for AI-powered appeal assistance and triage."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize AI service with optional API key."""
        self.api_key = api_key
    
    def generate_appeal_suggestions(
        self,
        evaluation: Evaluation,
        agent_initial_thoughts: str = ""
    ) -> AIAppealSuggestion:
        """
        Generate AI-powered suggestions for creating an appeal.
        
        Args:
            evaluation: The evaluation being appealed
            agent_initial_thoughts: Agent's initial thoughts on the appeal
            
        Returns:
            AIAppealSuggestion with recommendations
        """
        # In production, this would call OpenAI API
        # For now, we'll create intelligent mock suggestions based on the evaluation
        
        suggested_points = []
        
        # Analyze the evaluation feedback to suggest points
        if evaluation.score < 50:
            suggested_points.append(
                f"Request clarification on specific areas where improvement is needed"
            )
        
        if "unclear" in evaluation.feedback.lower() or "confusing" in evaluation.feedback.lower():
            suggested_points.append(
                "The feedback mentions unclear aspects - request specific examples"
            )
        
        if evaluation.score < 70:
            suggested_points.append(
                f"Highlight any constraints or challenges faced during the task"
            )
            suggested_points.append(
                f"Provide additional context that may not have been visible to the evaluator"
            )
        
        # Add general suggestions
        suggested_points.append(
            "Reference specific parts of your work that demonstrate competency"
        )
        
        # Assess strength based on score gap
        score_gap = 70 - evaluation.score  # Assuming 70 is passing threshold
        strength = "strong" if score_gap > 20 else "moderate" if score_gap > 10 else "weak"
        
        tone_recommendation = (
            "professional and fact-based" if evaluation.score < 50 
            else "respectful while highlighting strengths"
        )
        
        additional_context = []
        if not evaluation.criteria:
            additional_context.append("Request detailed evaluation criteria")
        if len(evaluation.feedback) < 100:
            additional_context.append("Request more detailed feedback")
        
        estimated_probability = min(0.9, max(0.1, (score_gap / 50) * 0.8))
        
        return AIAppealSuggestion(
            suggested_points=suggested_points,
            tone_recommendation=tone_recommendation,
            strength_assessment=f"This appeal appears to have {strength} merit based on the evaluation details",
            additional_context_needed=additional_context,
            estimated_success_probability=estimated_probability
        )
    
    def analyze_appeal_for_triage(
        self,
        appeal: Appeal,
        evaluation: Evaluation,
        agent_history: Optional[dict] = None
    ) -> AITriageAnalysis:
        """
        Generate AI-powered triage analysis for supervisor.
        
        Args:
            appeal: The appeal to analyze
            evaluation: The original evaluation
            agent_history: Optional history of the agent's past appeals
            
        Returns:
            AITriageAnalysis with recommendations
        """
        # In production, this would call OpenAI API for sophisticated analysis
        # For now, we'll create intelligent mock analysis
        
        key_points = []
        red_flags = []
        supporting_factors = []
        
        # Analyze appeal content
        if len(appeal.reason) < 50:
            red_flags.append("Appeal reason is very brief - may lack substance")
        else:
            supporting_factors.append("Detailed appeal reasoning provided")
        
        if len(appeal.supporting_evidence) > 0:
            supporting_factors.append(f"{len(appeal.supporting_evidence)} pieces of supporting evidence provided")
        else:
            red_flags.append("No supporting evidence provided")
        
        # Analyze evaluation
        score_gap = 70 - evaluation.score
        if score_gap > 20:
            key_points.append(f"Significant score gap ({score_gap} points from passing)")
            priority_rec = AppealPriority.HIGH
        elif score_gap > 10:
            key_points.append(f"Moderate score gap ({score_gap} points from passing)")
            priority_rec = AppealPriority.MEDIUM
        else:
            key_points.append(f"Small score gap ({score_gap} points from passing)")
            priority_rec = AppealPriority.LOW
        
        # Check evaluation feedback quality
        if len(evaluation.feedback) < 100:
            key_points.append("Original evaluation feedback is brief - may warrant reconsideration")
            supporting_factors.append("Limited original feedback suggests need for review")
        
        # Analyze agent history
        if agent_history and agent_history.get("past_appeals", 0) > 3:
            red_flags.append(f"Agent has {agent_history['past_appeals']} previous appeals")
        
        # Calculate validity score
        validity_score = 0.5  # Base score
        validity_score += len(supporting_factors) * 0.1
        validity_score -= len(red_flags) * 0.15
        validity_score = max(0.0, min(1.0, validity_score))
        
        # Recommend action
        if validity_score > 0.7:
            recommended_action = "Approve with modified score"
        elif validity_score > 0.5:
            recommended_action = "Review in detail - merit unclear"
        elif validity_score > 0.3:
            recommended_action = "Request additional information"
        else:
            recommended_action = "Likely reject - insufficient merit"
        
        # Estimate review time
        complexity = len(appeal.supporting_evidence) + (len(appeal.reason) // 100)
        estimated_time = 5 + (complexity * 2)
        
        return AITriageAnalysis(
            appeal_id=appeal.id,
            priority_recommendation=priority_rec,
            validity_score=validity_score,
            key_points=key_points,
            red_flags=red_flags,
            supporting_factors=supporting_factors,
            recommended_action=recommended_action,
            estimated_review_time_minutes=estimated_time,
            similar_past_cases=[]
        )
    
    def generate_decision_draft(
        self,
        appeal: Appeal,
        triage_analysis: AITriageAnalysis,
        decision_type: str
    ) -> str:
        """
        Generate a draft decision message for the supervisor.
        
        Args:
            appeal: The appeal
            triage_analysis: The triage analysis
            decision_type: 'approve', 'reject', or 'more_info'
            
        Returns:
            Draft decision message
        """
        if decision_type == 'approve':
            return (
                f"After careful review, your appeal has merit. "
                f"Key factors supporting this decision: {', '.join(triage_analysis.supporting_factors)}. "
                f"We will re-evaluate your work considering the additional context provided."
            )
        elif decision_type == 'reject':
            reasons = triage_analysis.red_flags if triage_analysis.red_flags else ["insufficient evidence provided"]
            return (
                f"After thorough review, we are unable to approve this appeal. "
                f"Reasons: {', '.join(reasons)}. "
                f"We encourage you to focus on the feedback provided in the original evaluation."
            )
        else:  # more_info
            return (
                f"We need additional information to properly evaluate your appeal. "
                f"Please provide: {', '.join(triage_analysis.key_points)}. "
                f"Once we receive this information, we will promptly review your appeal."
            )
