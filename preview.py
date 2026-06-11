#!/usr/bin/env python3
"""
Web-based preview interface for the Evaluation Appeal System.
Run this to see the system in action with a visual interface.
"""
from flask import Flask, render_template, jsonify, request
from datetime import datetime
import uuid

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

app = Flask(__name__)

# Initialize services
ai_service = AIService()
appeal_service = AppealService(ai_service)
supervisor_service = SupervisorService(ai_service, appeal_service.appeals)

# Create sample users
sample_agent = User(
    id="agent_demo",
    name="Alice Johnson",
    email="alice@example.com",
    role=UserRole.AGENT
)

sample_supervisor = User(
    id="supervisor_demo",
    name="Bob Smith",
    email="bob@example.com",
    role=UserRole.SUPERVISOR
)

# Create sample evaluation
sample_evaluation = Evaluation(
    id="eval_demo",
    agent_id=sample_agent.id,
    evaluator_id="evaluator_001",
    status=EvaluationStatus.FAILED,
    score=55.0,
    feedback="Performance did not meet expectations. Communication was unclear and task completion was delayed. Several quality issues were identified.",
    criteria={
        "quality": 50,
        "timeliness": 55,
        "communication": 60
    },
    evaluated_at=datetime.now(),
    task_description="Customer service call handling evaluation"
)


@app.route('/')
def index():
    """Home page with system overview."""
    return render_template('index.html')


@app.route('/agent')
def agent_view():
    """Agent view for creating appeals."""
    return render_template('agent.html', 
                         agent=sample_agent,
                         evaluation=sample_evaluation)


@app.route('/supervisor')
def supervisor_view():
    """Supervisor view for triaging appeals."""
    return render_template('supervisor.html',
                         supervisor=sample_supervisor)


@app.route('/api/create_appeal', methods=['POST'])
def create_appeal():
    """API endpoint to create an appeal with AI assistance."""
    data = request.json
    initial_thoughts = data.get('initial_thoughts', '')
    
    # Create draft with AI suggestions
    appeal, ai_suggestion = appeal_service.create_appeal_draft(
        sample_agent,
        sample_evaluation,
        initial_thoughts
    )
    
    return jsonify({
        'appeal_id': appeal.id,
        'ai_suggestion': {
            'suggested_points': ai_suggestion.suggested_points,
            'tone_recommendation': ai_suggestion.tone_recommendation,
            'strength_assessment': ai_suggestion.strength_assessment,
            'additional_context_needed': ai_suggestion.additional_context_needed,
            'estimated_success_probability': ai_suggestion.estimated_success_probability
        }
    })


@app.route('/api/submit_appeal', methods=['POST'])
def submit_appeal():
    """API endpoint to submit an appeal."""
    data = request.json
    appeal_id = data.get('appeal_id')
    reason = data.get('reason', '')
    evidence = data.get('evidence', [])
    priority = data.get('priority', 'medium')
    
    # Update and submit
    appeal_service.update_appeal_draft(
        appeal_id,
        reason=reason,
        supporting_evidence=evidence,
        priority=AppealPriority(priority)
    )
    
    appeal = appeal_service.submit_appeal(appeal_id)
    
    return jsonify({
        'success': True,
        'appeal_id': appeal.id,
        'status': appeal.status.value
    })


@app.route('/api/pending_appeals')
def get_pending_appeals():
    """API endpoint to get pending appeals with AI analysis."""
    pending = supervisor_service.get_pending_appeals(sort_by="priority")
    
    appeals_data = []
    for appeal, analysis in pending:
        appeals_data.append({
            'appeal_id': appeal.id,
            'agent_id': appeal.agent_id,
            'reason': appeal.reason,
            'status': appeal.status.value,
            'priority': appeal.priority.value,
            'supporting_evidence': appeal.supporting_evidence,
            'created_at': appeal.created_at.isoformat(),
            'submitted_at': appeal.submitted_at.isoformat() if appeal.submitted_at else None,
            'analysis': {
                'validity_score': analysis.validity_score,
                'priority_recommendation': analysis.priority_recommendation.value,
                'key_points': analysis.key_points,
                'red_flags': analysis.red_flags,
                'supporting_factors': analysis.supporting_factors,
                'recommended_action': analysis.recommended_action,
                'estimated_review_time_minutes': analysis.estimated_review_time_minutes
            }
        })
    
    return jsonify({'appeals': appeals_data})


@app.route('/api/decision_draft', methods=['POST'])
def get_decision_draft():
    """API endpoint to get AI-generated decision draft."""
    data = request.json
    appeal_id = data.get('appeal_id')
    decision_type = data.get('decision_type', 'approve')
    
    draft = supervisor_service.get_decision_draft(appeal_id, decision_type)
    
    return jsonify({'draft': draft})


@app.route('/api/make_decision', methods=['POST'])
def make_decision():
    """API endpoint to make a decision on an appeal."""
    data = request.json
    appeal_id = data.get('appeal_id')
    decision_type = data.get('decision_type')
    reason = data.get('reason', '')
    
    # Map decision type to status
    decision_map = {
        'approve': AppealStatus.APPROVED,
        'reject': AppealStatus.REJECTED,
        'more_info': AppealStatus.MORE_INFO_REQUESTED
    }
    
    decision = supervisor_service.make_decision(
        sample_supervisor,
        appeal_id,
        decision_map[decision_type],
        reason,
        action_items=data.get('action_items', [])
    )
    
    return jsonify({
        'success': True,
        'decision': decision.decision.value,
        'decided_at': decision.decided_at.isoformat()
    })


@app.route('/api/statistics')
def get_statistics():
    """API endpoint to get system statistics."""
    stats = supervisor_service.get_summary_statistics()
    return jsonify(stats)


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🌐 EVALUATION APPEAL SYSTEM - WEB PREVIEW")
    print("=" * 80)
    print("\n📱 Access the preview at: http://localhost:5000")
    print("\n   Available views:")
    print("   • Home:       http://localhost:5000/")
    print("   • Agent:      http://localhost:5000/agent")
    print("   • Supervisor: http://localhost:5000/supervisor")
    print("\n⏹  Press Ctrl+C to stop the server")
    print("=" * 80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
