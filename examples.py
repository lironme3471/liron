#!/usr/bin/env python3
"""
Example usage of the Evaluation Appeal System.
This script demonstrates various workflows and features.
"""
from datetime import datetime

from appeal_system import (
    AIService,
    AppealService,
    SupervisorService,
    User,
    UserRole,
    Evaluation,
    EvaluationStatus,
    AppealStatus,
    AppealPriority,
)


def example_agent_workflow():
    """
    Example: Agent creates and submits an appeal.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 1: Agent Appeal Workflow")
    print("=" * 80 + "\n")
    
    # Setup
    ai_service = AIService()
    appeal_service = AppealService(ai_service)
    
    agent = User(
        id="agent_123",
        name="Jane Doe",
        email="jane@company.com",
        role=UserRole.AGENT
    )
    
    evaluation = Evaluation(
        id="eval_123",
        agent_id=agent.id,
        evaluator_id="eval_456",
        status=EvaluationStatus.FAILED,
        score=62.0,
        feedback="Performance did not meet the quality standards expected.",
        criteria={"quality": 60, "communication": 65, "timeliness": 60},
        evaluated_at=datetime.now(),
        task_description="Technical support ticket resolution"
    )
    
    print(f"Agent: {agent.name}")
    print(f"Evaluation Score: {evaluation.score}/100")
    print(f"Status: {evaluation.status.value}\n")
    
    # Step 1: Create draft with AI help
    print("Step 1: Creating appeal draft with AI assistance...")
    appeal, suggestions = appeal_service.create_appeal_draft(
        agent,
        evaluation,
        initial_thoughts="I believe the evaluation criteria were not clearly communicated."
    )
    
    print(f"✓ Draft created (ID: {appeal.id[:8]}...)")
    print(f"  AI Success Probability: {suggestions.estimated_success_probability:.0%}")
    print(f"  AI Suggested {len(suggestions.suggested_points)} points")
    
    # Step 2: Refine the appeal
    print("\nStep 2: Refining the appeal with details...")
    appeal_service.update_appeal_draft(
        appeal.id,
        reason=(
            "I believe this evaluation does not reflect my actual performance. "
            "The criteria were not clearly defined at the start of the task, "
            "and I completed all primary objectives within the time frame. "
            "The issues mentioned were due to system limitations, not performance."
        ),
        supporting_evidence=[
            "Task completion report showing 100% completion",
            "Screenshots of system errors encountered",
            "Email chain with unclear requirements"
        ],
        priority=AppealPriority.HIGH
    )
    print("✓ Appeal updated with detailed reasoning and evidence")
    
    # Step 3: Submit
    print("\nStep 3: Submitting appeal...")
    final_appeal = appeal_service.submit_appeal(appeal.id)
    print(f"✓ Appeal submitted successfully!")
    print(f"  Status: {final_appeal.status.value}")
    print(f"  Submitted at: {final_appeal.submitted_at}")
    
    return appeal_service, appeal.id


def example_supervisor_workflow(appeal_service, appeal_id):
    """
    Example: Supervisor reviews and decides on appeal.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Supervisor Triage and Decision Workflow")
    print("=" * 80 + "\n")
    
    # Setup
    ai_service = AIService()
    supervisor_service = SupervisorService(ai_service, appeal_service.appeals)
    
    supervisor = User(
        id="super_123",
        name="John Manager",
        email="john@company.com",
        role=UserRole.SUPERVISOR
    )
    
    print(f"Supervisor: {supervisor.name}\n")
    
    # Step 1: View pending appeals
    print("Step 1: Reviewing pending appeals with AI analysis...")
    pending_appeals = supervisor_service.get_pending_appeals(sort_by="priority")
    
    for appeal, analysis in pending_appeals:
        print(f"\nAppeal ID: {appeal.id[:8]}...")
        print(f"  Validity Score: {analysis.validity_score:.0%}")
        print(f"  Priority: {analysis.priority_recommendation.value}")
        print(f"  Recommended Action: {analysis.recommended_action}")
        print(f"  Review Time Estimate: {analysis.estimated_review_time_minutes} min")
        
        if analysis.supporting_factors:
            print(f"  Supporting Factors: {len(analysis.supporting_factors)}")
        if analysis.red_flags:
            print(f"  Red Flags: {len(analysis.red_flags)}")
    
    # Step 2: Get AI-generated decision draft
    print("\nStep 2: Getting AI-generated decision draft...")
    draft = supervisor_service.get_decision_draft(appeal_id, 'approve')
    print(f"✓ Draft generated")
    print(f"  Preview: {draft[:100]}...")
    
    # Step 3: Make decision
    print("\nStep 3: Making final decision...")
    decision = supervisor_service.make_decision(
        supervisor,
        appeal_id,
        AppealStatus.APPROVED,
        reason=draft,
        action_items=[
            "Re-evaluate with consideration for system limitations",
            "Provide additional training on documentation"
        ]
    )
    
    print(f"✓ Decision recorded!")
    print(f"  Decision: {decision.decision.value}")
    print(f"  Action Items: {len(decision.action_items)}")
    
    # Step 4: View statistics
    print("\nStep 4: Viewing dashboard statistics...")
    stats = supervisor_service.get_summary_statistics()
    print(f"✓ Statistics retrieved")
    print(f"  Total Appeals: {stats['total_appeals']}")
    print(f"  Pending: {stats['pending_appeals']}")
    print(f"  Approved: {stats['approved']}")
    print(f"  Rejected: {stats['rejected']}")


def example_bulk_triage():
    """
    Example: Supervisor performs bulk triage on multiple appeals.
    """
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Bulk Triage Workflow")
    print("=" * 80 + "\n")
    
    # Setup
    ai_service = AIService()
    appeal_service = AppealService(ai_service)
    supervisor_service = SupervisorService(ai_service, appeal_service.appeals)
    
    # Create multiple mock appeals
    agent = User(id="agent_456", name="Test Agent", email="test@company.com", role=UserRole.AGENT)
    
    evaluations = {}
    appeal_ids = []
    
    for i in range(3):
        eval_id = f"eval_{i}"
        evaluation = Evaluation(
            id=eval_id,
            agent_id=agent.id,
            evaluator_id="evaluator",
            status=EvaluationStatus.FAILED,
            score=50.0 + i * 5,
            feedback=f"Evaluation feedback {i}",
            criteria={},
            evaluated_at=datetime.now(),
            task_description=f"Task {i}"
        )
        evaluations[eval_id] = evaluation
        
        appeal, _ = appeal_service.create_appeal_draft(
            agent,
            evaluation,
            f"Appeal reason {i} with sufficient length to pass validation"
        )
        appeal_service.submit_appeal(appeal.id)
        appeal_ids.append(appeal.id)
    
    print(f"Created {len(appeal_ids)} test appeals\n")
    
    # Perform bulk triage
    print("Performing bulk triage analysis...")
    analyses = supervisor_service.bulk_triage(appeal_ids, evaluations)
    
    print(f"✓ Analyzed {len(analyses)} appeals")
    print("\nResults:")
    for appeal_id, analysis in analyses.items():
        print(f"  {appeal_id[:8]}... -> Validity: {analysis.validity_score:.0%}, "
              f"Priority: {analysis.priority_recommendation.value}")


def main():
    """Run all examples."""
    print("\n" + "=" * 80)
    print("EVALUATION APPEAL SYSTEM - COMPREHENSIVE EXAMPLES")
    print("=" * 80)
    
    # Run examples
    appeal_service, appeal_id = example_agent_workflow()
    example_supervisor_workflow(appeal_service, appeal_id)
    example_bulk_triage()
    
    print("\n" + "=" * 80)
    print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
