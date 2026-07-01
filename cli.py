#!/usr/bin/env python3
"""
CLI interface for the Evaluation Appeal System.
Demonstrates agent and supervisor workflows.
"""
import argparse
from datetime import datetime
from typing import Optional

from appeal_system import (
    AIService,
    AppealService,
    SupervisorService,
    User,
    UserRole,
    Evaluation,
    EvaluationStatus,
    AppealStatus,
)


def print_separator():
    """Print a visual separator."""
    print("\n" + "=" * 80 + "\n")


def agent_create_appeal(
    appeal_service: AppealService,
    agent: User,
    evaluation: Evaluation,
    initial_thoughts: str
):
    """Agent workflow: Create an appeal with AI assistance."""
    print(f"🤖 Agent: {agent.name} is creating an appeal...")
    print_separator()
    
    # Create draft with AI suggestions
    appeal, ai_suggestion = appeal_service.create_appeal_draft(
        agent,
        evaluation,
        initial_thoughts
    )
    
    print("📝 AI-POWERED APPEAL SUGGESTIONS")
    print(f"\nStrength Assessment: {ai_suggestion.strength_assessment}")
    print(f"Success Probability: {ai_suggestion.estimated_success_probability:.0%}")
    print(f"\nRecommended Tone: {ai_suggestion.tone_recommendation}")
    
    print("\n💡 Suggested Points to Include:")
    for i, point in enumerate(ai_suggestion.suggested_points, 1):
        print(f"  {i}. {point}")
    
    if ai_suggestion.additional_context_needed:
        print("\n⚠️  Additional Context Needed:")
        for item in ai_suggestion.additional_context_needed:
            print(f"  • {item}")
    
    print_separator()
    
    # Update draft with more details
    full_reason = f"{initial_thoughts}\n\nBased on AI suggestions, I would like to add:\n"
    full_reason += "• I encountered unexpected technical constraints during the task\n"
    full_reason += "• The evaluation criteria were not clearly communicated beforehand\n"
    full_reason += "• My work met the primary objectives despite the lower score"
    
    appeal_service.update_appeal_draft(
        appeal.id,
        reason=full_reason,
        supporting_evidence=[
            "Task completion logs showing all objectives met",
            "Email thread showing unclear requirements",
            "Comparison with previous successful evaluations"
        ]
    )
    
    # Submit appeal
    appeal_service.submit_appeal(appeal.id)
    
    print(f"✅ Appeal {appeal.id} submitted successfully!")
    print(f"\nStatus: {appeal.status.value}")
    print(f"Priority: {appeal.priority.value}")
    
    return appeal


def supervisor_triage_appeals(
    supervisor_service: SupervisorService,
    supervisor: User
):
    """Supervisor workflow: Triage and review appeals."""
    print(f"👔 Supervisor: {supervisor.name} is reviewing appeals...")
    print_separator()
    
    # Get pending appeals with AI analysis
    pending_appeals = supervisor_service.get_pending_appeals(sort_by="priority")
    
    if not pending_appeals:
        print("📭 No pending appeals to review.")
        return
    
    print(f"📊 PENDING APPEALS: {len(pending_appeals)} total")
    print_separator()
    
    for i, (appeal, analysis) in enumerate(pending_appeals, 1):
        print(f"\n🔍 APPEAL #{i} - ID: {appeal.id[:8]}...")
        print(f"   Agent: {appeal.agent_id}")
        print(f"   Submitted: {appeal.submitted_at}")
        print(f"   Priority: {appeal.priority.value} (AI Recommends: {analysis.priority_recommendation.value})")
        
        print(f"\n   🤖 AI ANALYSIS:")
        print(f"      Validity Score: {analysis.validity_score:.0%}")
        print(f"      Recommended Action: {analysis.recommended_action}")
        print(f"      Estimated Review Time: {analysis.estimated_review_time_minutes} minutes")
        
        if analysis.key_points:
            print(f"\n      Key Points:")
            for point in analysis.key_points:
                print(f"        • {point}")
        
        if analysis.supporting_factors:
            print(f"\n      ✅ Supporting Factors:")
            for factor in analysis.supporting_factors:
                print(f"        • {factor}")
        
        if analysis.red_flags:
            print(f"\n      🚩 Red Flags:")
            for flag in analysis.red_flags:
                print(f"        • {flag}")
        
        print_separator()
    
    # Show summary statistics
    stats = supervisor_service.get_summary_statistics()
    print("\n📈 SUMMARY STATISTICS")
    print(f"   Total Appeals: {stats['total_appeals']}")
    print(f"   Pending: {stats['pending_appeals']}")
    print(f"   Approved: {stats['approved']}")
    print(f"   Rejected: {stats['rejected']}")
    print(f"   Avg Review Time: {stats['avg_review_time_estimate']:.1f} minutes")


def supervisor_decide_appeal(
    supervisor_service: SupervisorService,
    supervisor: User,
    appeal_id: str,
    decision_type: str
):
    """Supervisor workflow: Make a decision on an appeal."""
    print(f"👔 Supervisor: {supervisor.name} is deciding on appeal {appeal_id[:8]}...")
    print_separator()
    
    # Get AI-generated decision draft
    draft_message = supervisor_service.get_decision_draft(appeal_id, decision_type)
    
    print("📝 AI-GENERATED DECISION DRAFT:")
    print(f"\n{draft_message}\n")
    print_separator()
    
    # Map decision type to status
    decision_map = {
        'approve': AppealStatus.APPROVED,
        'reject': AppealStatus.REJECTED,
        'more_info': AppealStatus.MORE_INFO_REQUESTED
    }
    
    decision_status = decision_map[decision_type]
    
    # Make decision
    decision = supervisor_service.make_decision(
        supervisor,
        appeal_id,
        decision_status,
        draft_message,
        action_items=["Re-evaluate with new context", "Provide detailed feedback"]
    )
    
    print(f"✅ Decision recorded successfully!")
    print(f"\nDecision: {decision.decision.value}")
    print(f"Decided at: {decision.decided_at}")
    print(f"Action Items: {len(decision.action_items)}")


def run_demo():
    """Run a complete demo of the system."""
    print("🎯 EVALUATION APPEAL SYSTEM DEMO")
    print("=" * 80)
    
    # Initialize services
    ai_service = AIService()
    appeal_service = AppealService(ai_service)
    supervisor_service = SupervisorService(ai_service, appeal_service.appeals)
    
    # Create users
    agent = User(
        id="agent_001",
        name="Alice Johnson",
        email="alice@example.com",
        role=UserRole.AGENT
    )
    
    supervisor = User(
        id="supervisor_001",
        name="Bob Smith",
        email="bob@example.com",
        role=UserRole.SUPERVISOR
    )
    
    # Create a mock evaluation
    evaluation = Evaluation(
        id="eval_001",
        agent_id=agent.id,
        evaluator_id="evaluator_123",
        status=EvaluationStatus.FAILED,
        score=55.0,
        feedback=(
            "Performance did not meet expectations. "
            "Communication was unclear and task completion was delayed. "
            "Several quality issues were identified."
        ),
        criteria={
            "quality": 50,
            "timeliness": 55,
            "communication": 60
        },
        evaluated_at=datetime.now(),
        task_description="Customer service call handling evaluation"
    )
    
    # PART 1: Agent creates appeal with AI assistance
    print("\n📱 PART 1: AGENT APPEAL CREATION WITH AI ASSISTANCE")
    print_separator()
    
    initial_thoughts = (
        "I believe this evaluation does not accurately reflect my performance. "
        "There were several factors outside my control that affected the outcome."
    )
    
    appeal = agent_create_appeal(appeal_service, agent, evaluation, initial_thoughts)
    
    # PART 2: Supervisor triages appeals
    print("\n\n👔 PART 2: SUPERVISOR TRIAGE WITH AI ANALYSIS")
    print_separator()
    
    supervisor_triage_appeals(supervisor_service, supervisor)
    
    # PART 3: Supervisor makes a decision
    print("\n\n⚖️  PART 3: SUPERVISOR DECISION WITH AI ASSISTANCE")
    print_separator()
    
    supervisor_decide_appeal(supervisor_service, supervisor, appeal.id, 'approve')
    
    print("\n\n✨ DEMO COMPLETE!")
    print("=" * 80)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Evaluation Appeal System CLI"
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run a complete demo of the system"
    )
    
    args = parser.parse_args()
    
    if args.demo:
        run_demo()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
