# Evaluation Appeal System with AI Assistance

A comprehensive system for agents to appeal evaluations with AI-powered suggestions, and for supervisors to efficiently triage and decide on appeals.

## 🎯 Preview the Project

**Try it now with the interactive web interface:**

```bash
python preview.py
```

Visit http://localhost:5000 to explore the system with a visual interface!

### Screenshots

**Home Page:**
![Home Page](https://github.com/user-attachments/assets/b0f092a9-25dd-432c-bc79-cb1ec20b7d15)

**Agent View - Create Appeal:**
![Agent View](https://github.com/user-attachments/assets/54e8eca7-7ff2-4324-9673-198a3b331657)

**Supervisor View - Triage Appeals:**
![Supervisor View](https://github.com/user-attachments/assets/3222ae6b-44ae-4d9c-8f75-8a801632d0c8)

## Features

### Agent-Side Features
- **AI-Assisted Appeal Creation**: Get intelligent suggestions on how to structure your appeal
- **Real-time Success Probability**: AI estimates the likelihood of appeal success
- **Tone and Content Recommendations**: AI suggests the best approach and key points to include
- **Draft and Submit Workflow**: Create drafts, refine them, and submit when ready
- **Appeal Tracking**: Monitor the status of your appeals

### Supervisor-Side Features
- **AI-Powered Triage**: Automatic analysis and prioritization of incoming appeals
- **Validity Scoring**: AI assesses the merit of each appeal
- **Quick Decision Workflow**: Streamlined approve/reject/request-more-info flow
- **Decision Drafts**: AI-generated response templates for faster decisions
- **Bulk Operations**: Triage multiple appeals efficiently
- **Dashboard Statistics**: Overview of appeal metrics and trends

## Installation

1. Clone the repository:
```bash
git clone https://github.com/lironme3471/liron.git
cd liron
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install the package:
```bash
pip install -e .
```

## Usage

### 🌐 Web Preview (Recommended)

The best way to explore the system with a visual interface:

```bash
python preview.py
```

Then open your browser to:
- **Home**: http://localhost:5000/
- **Agent View**: http://localhost:5000/agent
- **Supervisor View**: http://localhost:5000/supervisor

This provides an interactive web interface where you can:
- Create appeals as an agent with real-time AI suggestions
- View pending appeals as a supervisor with AI triage analysis
- Make decisions with AI-generated draft responses
- See the full workflow in action

### 📱 CLI Demo

Run a complete workflow demonstration in the terminal:

```bash
python cli.py --demo
```

This will show:
1. An agent creating an appeal with AI assistance
2. A supervisor triaging pending appeals
3. A supervisor making a decision on an appeal

### Programmatic Usage

#### Agent Workflow Example

```python
from appeal_system import AIService, AppealService, User, UserRole, Evaluation

# Initialize services
ai_service = AIService()
appeal_service = AppealService(ai_service)

# Create agent user
agent = User(
    id="agent_001",
    name="Alice Johnson",
    email="alice@example.com",
    role=UserRole.AGENT
)

# Create evaluation (mock)
evaluation = Evaluation(...)

# Create appeal draft with AI suggestions
appeal, ai_suggestions = appeal_service.create_appeal_draft(
    agent,
    evaluation,
    initial_thoughts="I believe this evaluation was unfair..."
)

# Review AI suggestions
print(f"Success probability: {ai_suggestions.estimated_success_probability:.0%}")
print("Suggested points:", ai_suggestions.suggested_points)

# Update draft with more details
appeal_service.update_appeal_draft(
    appeal.id,
    reason="Updated detailed reason...",
    supporting_evidence=["doc1.pdf", "email.txt"]
)

# Submit the appeal
appeal_service.submit_appeal(appeal.id)
```

#### Supervisor Workflow Example

```python
from appeal_system import SupervisorService, AppealStatus

# Initialize supervisor service
supervisor_service = SupervisorService(ai_service, appeal_service.appeals)

# Create supervisor user
supervisor = User(
    id="supervisor_001",
    name="Bob Smith",
    email="bob@example.com",
    role=UserRole.SUPERVISOR
)

# Get pending appeals with AI analysis
pending_appeals = supervisor_service.get_pending_appeals(sort_by="priority")

for appeal, analysis in pending_appeals:
    print(f"Appeal {appeal.id}")
    print(f"Validity score: {analysis.validity_score:.0%}")
    print(f"Recommended action: {analysis.recommended_action}")
    print(f"Review time estimate: {analysis.estimated_review_time_minutes} min")

# Get AI-generated decision draft
draft_message = supervisor_service.get_decision_draft(
    appeal.id,
    decision_type='approve'
)

# Make a decision
decision = supervisor_service.make_decision(
    supervisor,
    appeal.id,
    AppealStatus.APPROVED,
    reason=draft_message,
    action_items=["Re-evaluate with new context"]
)
```

## Architecture

The system consists of several key components:

### Data Models (`models.py`)
- **User**: Represents agents and supervisors
- **Evaluation**: Represents performance evaluations
- **Appeal**: Represents an appeal with AI assistance
- **AIAppealSuggestion**: AI-generated suggestions for agents
- **AITriageAnalysis**: AI-generated analysis for supervisors
- **SupervisorDecision**: Records supervisor decisions

### Services

#### AI Service (`ai_service.py`)
Provides AI-powered assistance for both agents and supervisors:
- Generates appeal suggestions and success probability estimates
- Analyzes appeals for triage with validity scoring
- Creates decision draft messages

#### Appeal Service (`appeal_service.py`)
Manages the agent-side appeal workflow:
- Create appeal drafts with AI suggestions
- Update and refine appeals
- Submit appeals for review
- Track appeal status

#### Supervisor Service (`supervisor_service.py`)
Manages the supervisor-side triage and decision workflow:
- List and filter pending appeals
- Get AI-powered triage analysis
- Make decisions (approve/reject/request more info)
- Generate decision drafts
- Bulk triage operations
- Summary statistics

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or using unittest:

```bash
python -m unittest discover tests/
```

## AI Integration

The current implementation includes a sophisticated mock AI service that demonstrates the capabilities. In a production environment, you would integrate with:

- **OpenAI GPT-4** for natural language understanding and generation
- **Custom ML models** trained on historical appeal data
- **Sentiment analysis** for tone recommendations
- **Pattern recognition** for similar case identification

To integrate with OpenAI:

```python
ai_service = AIService(api_key="your-openai-api-key")
```

Then modify the `ai_service.py` to call the actual OpenAI API instead of using the mock implementation.

## Key Design Decisions

1. **AI-First Approach**: AI assistance is integrated throughout the workflow, not bolted on
2. **Separation of Concerns**: Clear boundaries between agent, supervisor, and AI services
3. **Pydantic Models**: Type-safe data models with validation
4. **Status Machine**: Clear appeal states with defined transitions
5. **Extensibility**: Easy to add new AI capabilities or decision factors

## Future Enhancements

- [ ] Integration with actual OpenAI API
- [ ] Historical appeal database for learning
- [ ] Similar case detection using embeddings
- [ ] Multi-supervisor consensus workflows
- [ ] Agent feedback loop on AI suggestions
- [ ] Performance metrics and A/B testing
- [ ] Web UI for both agents and supervisors
- [ ] Email notifications for status changes
- [ ] Appeal templates based on evaluation types

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details