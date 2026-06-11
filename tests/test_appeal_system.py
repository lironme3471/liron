"""
Unit tests for the evaluation appeal system.
"""
import unittest
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


class TestAIService(unittest.TestCase):
    """Tests for AI service."""
    
    def setUp(self):
        self.ai_service = AIService()
        self.evaluation = Evaluation(
            id="eval_001",
            agent_id="agent_001",
            evaluator_id="eval_001",
            status=EvaluationStatus.FAILED,
            score=45.0,
            feedback="Poor performance in multiple areas",
            criteria={"quality": 40, "speed": 50},
            evaluated_at=datetime.now(),
            task_description="Test task"
        )
    
    def test_generate_appeal_suggestions(self):
        """Test AI appeal suggestion generation."""
        suggestions = self.ai_service.generate_appeal_suggestions(
            self.evaluation,
            "I think the evaluation was unfair"
        )
        
        self.assertIsNotNone(suggestions)
        self.assertGreater(len(suggestions.suggested_points), 0)
        self.assertIsNotNone(suggestions.tone_recommendation)
        self.assertIsNotNone(suggestions.strength_assessment)
        self.assertGreaterEqual(suggestions.estimated_success_probability, 0)
        self.assertLessEqual(suggestions.estimated_success_probability, 1)
    
    def test_analyze_appeal_for_triage(self):
        """Test AI triage analysis generation."""
        from appeal_system.models import Appeal
        
        appeal = Appeal(
            id="appeal_001",
            evaluation_id="eval_001",
            agent_id="agent_001",
            status=AppealStatus.SUBMITTED,
            priority=AppealPriority.MEDIUM,
            reason="I believe the evaluation was unfair due to unclear requirements",
            supporting_evidence=["log1.txt", "email.txt"],
            created_at=datetime.now(),
            updated_at=datetime.now(),
            submitted_at=datetime.now()
        )
        
        analysis = self.ai_service.analyze_appeal_for_triage(
            appeal,
            self.evaluation
        )
        
        self.assertEqual(analysis.appeal_id, appeal.id)
        self.assertIsInstance(analysis.priority_recommendation, AppealPriority)
        self.assertGreaterEqual(analysis.validity_score, 0)
        self.assertLessEqual(analysis.validity_score, 1)
        self.assertGreater(len(analysis.key_points), 0)
        self.assertGreater(analysis.estimated_review_time_minutes, 0)


class TestAppealService(unittest.TestCase):
    """Tests for appeal service."""
    
    def setUp(self):
        self.ai_service = AIService()
        self.appeal_service = AppealService(self.ai_service)
        
        self.agent = User(
            id="agent_001",
            name="Test Agent",
            email="agent@test.com",
            role=UserRole.AGENT
        )
        
        self.evaluation = Evaluation(
            id="eval_001",
            agent_id=self.agent.id,
            evaluator_id="eval_001",
            status=EvaluationStatus.FAILED,
            score=45.0,
            feedback="Needs improvement",
            criteria={},
            evaluated_at=datetime.now(),
            task_description="Test task"
        )
    
    def test_create_appeal_draft(self):
        """Test creating an appeal draft with AI suggestions."""
        appeal, suggestions = self.appeal_service.create_appeal_draft(
            self.agent,
            self.evaluation,
            "Initial thoughts"
        )
        
        self.assertEqual(appeal.agent_id, self.agent.id)
        self.assertEqual(appeal.evaluation_id, self.evaluation.id)
        self.assertEqual(appeal.status, AppealStatus.DRAFT)
        self.assertIsNotNone(appeal.ai_suggestion)
        self.assertIsNotNone(suggestions)
    
    def test_update_appeal_draft(self):
        """Test updating an appeal draft."""
        appeal, _ = self.appeal_service.create_appeal_draft(
            self.agent,
            self.evaluation,
            "Initial thoughts"
        )
        
        updated_reason = "Updated detailed reason"
        evidence = ["doc1.pdf", "doc2.pdf"]
        
        updated_appeal = self.appeal_service.update_appeal_draft(
            appeal.id,
            reason=updated_reason,
            supporting_evidence=evidence,
            priority=AppealPriority.HIGH
        )
        
        self.assertEqual(updated_appeal.reason, updated_reason)
        self.assertEqual(updated_appeal.supporting_evidence, evidence)
        self.assertEqual(updated_appeal.priority, AppealPriority.HIGH)
    
    def test_submit_appeal(self):
        """Test submitting an appeal."""
        appeal, _ = self.appeal_service.create_appeal_draft(
            self.agent,
            self.evaluation,
            "This is a valid reason with more than 20 characters"
        )
        
        submitted_appeal = self.appeal_service.submit_appeal(appeal.id)
        
        self.assertEqual(submitted_appeal.status, AppealStatus.SUBMITTED)
        self.assertIsNotNone(submitted_appeal.submitted_at)
    
    def test_submit_appeal_validation(self):
        """Test appeal submission validation."""
        appeal, _ = self.appeal_service.create_appeal_draft(
            self.agent,
            self.evaluation,
            "Short"
        )
        
        with self.assertRaises(ValueError):
            self.appeal_service.submit_appeal(appeal.id)
    
    def test_list_agent_appeals(self):
        """Test listing agent's appeals."""
        # Create multiple appeals
        appeal1, _ = self.appeal_service.create_appeal_draft(
            self.agent,
            self.evaluation,
            "Reason 1 with enough characters"
        )
        self.appeal_service.submit_appeal(appeal1.id)
        
        appeal2, _ = self.appeal_service.create_appeal_draft(
            self.agent,
            self.evaluation,
            "Reason 2 with enough characters"
        )
        
        # List all appeals
        all_appeals = self.appeal_service.list_agent_appeals(self.agent.id)
        self.assertEqual(len(all_appeals), 2)
        
        # Filter by status
        submitted_appeals = self.appeal_service.list_agent_appeals(
            self.agent.id,
            status_filter=AppealStatus.SUBMITTED
        )
        self.assertEqual(len(submitted_appeals), 1)


class TestSupervisorService(unittest.TestCase):
    """Tests for supervisor service."""
    
    def setUp(self):
        self.ai_service = AIService()
        self.appeal_service = AppealService(self.ai_service)
        self.supervisor_service = SupervisorService(
            self.ai_service,
            self.appeal_service.appeals
        )
        
        self.agent = User(
            id="agent_001",
            name="Test Agent",
            email="agent@test.com",
            role=UserRole.AGENT
        )
        
        self.supervisor = User(
            id="supervisor_001",
            name="Test Supervisor",
            email="supervisor@test.com",
            role=UserRole.SUPERVISOR
        )
        
        self.evaluation = Evaluation(
            id="eval_001",
            agent_id=self.agent.id,
            evaluator_id="eval_001",
            status=EvaluationStatus.FAILED,
            score=45.0,
            feedback="Needs improvement",
            criteria={},
            evaluated_at=datetime.now(),
            task_description="Test task"
        )
    
    def test_get_pending_appeals(self):
        """Test getting pending appeals with triage."""
        # Create and submit an appeal
        appeal, _ = self.appeal_service.create_appeal_draft(
            self.agent,
            self.evaluation,
            "This is a valid reason for appeal with enough characters"
        )
        self.appeal_service.submit_appeal(appeal.id)
        
        # Get pending appeals
        pending = self.supervisor_service.get_pending_appeals()
        
        self.assertEqual(len(pending), 1)
        appeal, analysis = pending[0]
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis.appeal_id, appeal.id)
    
    def test_make_decision(self):
        """Test making a decision on an appeal."""
        # Create and submit an appeal
        appeal, _ = self.appeal_service.create_appeal_draft(
            self.agent,
            self.evaluation,
            "This is a valid reason for appeal with enough characters"
        )
        self.appeal_service.submit_appeal(appeal.id)
        
        # Make decision
        decision = self.supervisor_service.make_decision(
            self.supervisor,
            appeal.id,
            AppealStatus.APPROVED,
            "Approved after review",
            action_items=["Re-evaluate", "Provide feedback"]
        )
        
        self.assertEqual(decision.appeal_id, appeal.id)
        self.assertEqual(decision.decision, AppealStatus.APPROVED)
        self.assertEqual(decision.supervisor_id, self.supervisor.id)
        self.assertEqual(len(decision.action_items), 2)
        
        # Verify appeal was updated
        updated_appeal = self.appeal_service.get_appeal_status(appeal.id)
        self.assertEqual(updated_appeal.status, AppealStatus.APPROVED)
        self.assertEqual(updated_appeal.reviewed_by, self.supervisor.id)
    
    def test_get_decision_draft(self):
        """Test getting AI-generated decision draft."""
        # Create and submit an appeal
        appeal, _ = self.appeal_service.create_appeal_draft(
            self.agent,
            self.evaluation,
            "This is a valid reason for appeal with enough characters"
        )
        self.appeal_service.submit_appeal(appeal.id)
        
        # Get decision drafts
        approve_draft = self.supervisor_service.get_decision_draft(
            appeal.id,
            'approve'
        )
        reject_draft = self.supervisor_service.get_decision_draft(
            appeal.id,
            'reject'
        )
        
        self.assertIsInstance(approve_draft, str)
        self.assertGreater(len(approve_draft), 0)
        self.assertIsInstance(reject_draft, str)
        self.assertGreater(len(reject_draft), 0)
    
    def test_get_summary_statistics(self):
        """Test getting summary statistics."""
        # Create multiple appeals in different states
        appeal1, _ = self.appeal_service.create_appeal_draft(
            self.agent,
            self.evaluation,
            "Valid reason for appeal number one with enough characters"
        )
        self.appeal_service.submit_appeal(appeal1.id)
        
        appeal2, _ = self.appeal_service.create_appeal_draft(
            self.agent,
            self.evaluation,
            "Valid reason for appeal number two with enough characters"
        )
        self.appeal_service.submit_appeal(appeal2.id)
        
        self.supervisor_service.make_decision(
            self.supervisor,
            appeal1.id,
            AppealStatus.APPROVED,
            "Approved"
        )
        
        # Get statistics
        stats = self.supervisor_service.get_summary_statistics()
        
        self.assertEqual(stats['total_appeals'], 2)
        self.assertEqual(stats['pending_appeals'], 1)
        self.assertEqual(stats['approved'], 1)
        self.assertIn('status_breakdown', stats)
        self.assertIn('priority_breakdown', stats)


if __name__ == '__main__':
    unittest.main()
