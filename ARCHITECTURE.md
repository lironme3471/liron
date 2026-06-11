# System Architecture

## Overview

The Evaluation Appeal System is designed with a modular architecture that separates concerns between agent workflows, supervisor workflows, and AI assistance.

## Component Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     Application Layer                        │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface                    Examples & Demos          │
│  (cli.py)                         (examples.py)             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      Service Layer                           │
├───────────────────────────┬─────────────────────────────────┤
│   AppealService           │   SupervisorService             │
│   (Agent Workflows)       │   (Supervisor Workflows)        │
│                           │                                 │
│   • Create draft          │   • List pending appeals        │
│   • Update draft          │   • Triage analysis             │
│   • Submit appeal         │   • Make decisions              │
│   • Track status          │   • Bulk operations             │
└───────────────────────────┴─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      AI Service Layer                        │
├─────────────────────────────────────────────────────────────┤
│   AIService                                                  │
│   • Generate appeal suggestions                              │
│   • Analyze appeals for triage                               │
│   • Generate decision drafts                                 │
│   • Assess success probability                               │
│   • Priority recommendations                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       Data Layer                             │
├─────────────────────────────────────────────────────────────┤
│   Pydantic Models (models.py)                                │
│   • User, Evaluation, Appeal                                 │
│   • AIAppealSuggestion, AITriageAnalysis                     │
│   • SupervisorDecision                                       │
└─────────────────────────────────────────────────────────────┘
```

## Agent Workflow

```
┌──────────────┐
│ Agent starts │
│ with         │
│ evaluation   │
└──────┬───────┘
       │
       ▼
┌────────────────────────────┐
│ Request AI suggestions     │
│ • Success probability      │
│ • Key points to include    │
│ • Tone recommendations     │
└──────┬─────────────────────┘
       │
       ▼
┌────────────────────────────┐
│ Create appeal draft        │
│ • Initial thoughts         │
│ • AI suggestions attached  │
└──────┬─────────────────────┘
       │
       ▼
┌────────────────────────────┐
│ Refine draft               │
│ • Add detailed reason      │
│ • Include evidence         │
│ • Set priority             │
└──────┬─────────────────────┘
       │
       ▼
┌────────────────────────────┐
│ Submit appeal              │
│ Status: SUBMITTED          │
└──────┬─────────────────────┘
       │
       ▼
┌────────────────────────────┐
│ Track status               │
│ • Monitor progress         │
│ • Receive decision         │
└────────────────────────────┘
```

## Supervisor Workflow

```
┌────────────────────────────┐
│ View pending appeals       │
│ • Sorted by priority       │
│ • Filtered by criteria     │
└──────┬─────────────────────┘
       │
       ▼
┌────────────────────────────┐
│ AI Triage Analysis         │
│ • Validity score (0-100%)  │
│ • Priority recommendation  │
│ • Key points extraction    │
│ • Red flags identification │
│ • Supporting factors       │
│ • Review time estimate     │
└──────┬─────────────────────┘
       │
       ▼
┌────────────────────────────┐
│ Review specific appeal     │
│ • Read full details        │
│ • Consider AI analysis     │
│ • Review evidence          │
└──────┬─────────────────────┘
       │
       ▼
┌────────────────────────────┐
│ Get AI decision draft      │
│ • Pre-written response     │
│ • Customizable template    │
└──────┬─────────────────────┘
       │
       ▼
┌────────────────────────────┐
│ Make decision              │
│ • APPROVE                  │
│ • REJECT                   │
│ • REQUEST MORE INFO        │
└──────┬─────────────────────┘
       │
       ▼
┌────────────────────────────┐
│ Record decision            │
│ • Update appeal status     │
│ • Add action items         │
│ • Notify agent             │
└────────────────────────────┘
```

## AI Service Capabilities

### For Agents: Appeal Suggestions

The AI analyzes the evaluation and provides:

1. **Success Probability Estimation**
   - Based on score gap from passing threshold
   - Considers feedback quality and detail
   - Accounts for evidence provided

2. **Key Points Identification**
   - Suggests specific arguments to make
   - Identifies weaknesses in evaluation
   - Recommends areas to provide context

3. **Tone Recommendations**
   - Suggests appropriate communication style
   - Balances assertiveness with respect
   - Adapts to severity of situation

4. **Additional Context Requests**
   - Identifies missing information
   - Suggests what evidence to gather
   - Highlights evaluation gaps

### For Supervisors: Triage Analysis

The AI provides comprehensive appeal analysis:

1. **Validity Scoring (0-100%)**
   - Analyzes appeal substance
   - Considers evidence quality
   - Weighs supporting vs red flag factors

2. **Priority Recommendation**
   - URGENT: Critical cases requiring immediate attention
   - HIGH: Significant score gaps or strong merit
   - MEDIUM: Standard appeals with moderate merit
   - LOW: Minor issues or weak cases

3. **Key Points Extraction**
   - Identifies main arguments
   - Highlights critical information
   - Summarizes appeal essence

4. **Red Flags Detection**
   - Brief or vague reasoning
   - Lack of evidence
   - Pattern of frequent appeals
   - Inconsistencies

5. **Supporting Factors**
   - Detailed reasoning provided
   - Strong evidence attached
   - Original evaluation gaps
   - Valid contextual factors

6. **Review Time Estimation**
   - Based on complexity
   - Considers evidence amount
   - Accounts for detail level

7. **Recommended Actions**
   - Approve with modified score
   - Review in detail
   - Request additional information
   - Likely reject

## Data Flow

### Appeal Creation Flow

```
Agent → AppealService.create_appeal_draft()
    ↓
AIService.generate_appeal_suggestions(evaluation)
    ↓
Analysis of:
    • Score gap
    • Feedback quality
    • Evaluation criteria
    ↓
Return: Appeal + AIAppealSuggestion
    ↓
Agent reviews and refines
    ↓
AppealService.submit_appeal()
```

### Triage Flow

```
Supervisor → SupervisorService.get_pending_appeals()
    ↓
For each appeal:
    AIService.analyze_appeal_for_triage()
        ↓
    Analysis of:
        • Appeal content
        • Evidence quality
        • Agent history
        • Evaluation details
        ↓
    Return: AITriageAnalysis
    ↓
Sort by: Priority, Date, or Validity Score
    ↓
Present to supervisor with AI insights
```

### Decision Flow

```
Supervisor selects appeal
    ↓
SupervisorService.get_decision_draft(appeal_id, decision_type)
    ↓
AIService.generate_decision_draft()
    ↓
Returns pre-written message template
    ↓
Supervisor reviews/customizes
    ↓
SupervisorService.make_decision()
    ↓
Updates:
    • Appeal status
    • Review timestamp
    • Supervisor notes
    ↓
Creates SupervisorDecision record
```

## Extensibility Points

The system is designed to be easily extended:

1. **AI Service Integration**
   - Currently uses mock implementation
   - Can integrate OpenAI GPT-4 API
   - Can add custom ML models
   - Can incorporate historical data learning

2. **Storage Backend**
   - Currently uses in-memory storage
   - Can add database layer (PostgreSQL, MongoDB)
   - Can add caching (Redis)
   - Can add full-text search (Elasticsearch)

3. **Notification System**
   - Add email notifications
   - Add Slack/Teams integration
   - Add SMS alerts for urgent appeals
   - Add webhook support

4. **Web Interface**
   - Add REST API
   - Add GraphQL API
   - Add React/Vue frontend
   - Add real-time updates (WebSocket)

5. **Analytics**
   - Appeal success rate tracking
   - AI accuracy metrics
   - Review time analytics
   - Agent/Supervisor performance metrics

## Security Considerations

1. **Authentication & Authorization**
   - Role-based access control (Agent vs Supervisor)
   - Appeal ownership verification
   - Audit logging of all decisions

2. **Data Privacy**
   - Sensitive information handling
   - PII protection in AI processing
   - Secure storage of evaluation data

3. **Input Validation**
   - Pydantic models for type safety
   - Length constraints on text fields
   - Status transition validation

## Performance Optimization

1. **Bulk Operations**
   - Batch AI analysis for multiple appeals
   - Parallel processing support
   - Efficient filtering and sorting

2. **Caching Strategy**
   - Cache AI analysis results
   - Cache frequently accessed data
   - Invalidate on updates

3. **Scalability**
   - Stateless service design
   - Horizontal scaling support
   - Async processing for AI calls
