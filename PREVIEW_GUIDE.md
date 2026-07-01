# How to Preview the Evaluation Appeal System

This guide shows you how to preview and explore the Evaluation Appeal System.

## 🚀 Quick Start (3 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `pydantic` - Data validation
- `openai` - AI integration (for future use)
- `python-dateutil` - Date handling
- `flask` - Web framework for preview

### Step 2: Start the Preview Server
```bash
python preview.py
```

You should see:
```
================================================================================
🌐 EVALUATION APPEAL SYSTEM - WEB PREVIEW
================================================================================

📱 Access the preview at: http://localhost:5000

   Available views:
   • Home:       http://localhost:5000/
   • Agent:      http://localhost:5000/agent
   • Supervisor: http://localhost:5000/supervisor

⏹  Press Ctrl+C to stop the server
================================================================================
```

### Step 3: Open Your Browser
Navigate to **http://localhost:5000**

## 📋 What You Can Preview

### 1. Home Page (http://localhost:5000/)
- System overview and statistics
- Feature highlights for agents, supervisors, and AI
- Quick access to both agent and supervisor views

### 2. Agent View (http://localhost:5000/agent)

**Experience the agent workflow:**

1. **View Evaluation Details**
   - See the failed evaluation (55/100)
   - Review feedback and criteria

2. **Get AI Assistance**
   - Enter your initial thoughts
   - Click "Get AI Suggestions"
   - See real-time AI analysis:
     - Success probability estimate
     - Strength assessment
     - Tone recommendations
     - Suggested key points

3. **Complete Your Appeal**
   - Write detailed reasoning
   - Add supporting evidence
   - Set priority level
   - Submit for review

### 3. Supervisor View (http://localhost:5000/supervisor)

**Experience the supervisor workflow:**

1. **View Dashboard**
   - Total appeals count
   - Pending, approved, rejected stats
   - System overview

2. **Review Pending Appeals**
   - See AI-powered triage analysis
   - Validity scores (0-100%)
   - Priority recommendations
   - Key points and red flags
   - Supporting factors
   - Review time estimates

3. **Make Quick Decisions**
   - Click Approve, Reject, or Request More Info
   - Get AI-generated decision drafts
   - Customize and confirm decisions
   - Watch statistics update in real-time

## 🎨 Preview Features

### Beautiful UI
- Modern gradient design
- Responsive layout
- Clean, professional appearance
- Intuitive navigation

### Interactive Elements
- Real-time form validation
- Loading indicators
- Modal dialogs for decisions
- Dynamic content updates
- Smooth animations

### AI Visualizations
- Progress bars for probability scores
- Color-coded priority badges
- Validity score indicators
- Organized lists of factors

## 🔄 Testing the Full Workflow

### Create an Appeal as Agent:

1. Go to http://localhost:5000/agent
2. Enter: "I believe the evaluation criteria were not clearly communicated"
3. Click "Get AI Suggestions"
4. Review the AI analysis
5. Complete the form with:
   - Detailed reason
   - Evidence files
   - Priority level
6. Click "Submit Appeal"

### Review as Supervisor:

1. Go to http://localhost:5000/supervisor
2. Click "🔄 Refresh Appeals"
3. See your submitted appeal with AI analysis
4. Click one of the decision buttons
5. Review the AI-generated draft
6. Confirm the decision
7. Watch the appeal disappear and stats update

## 📱 Alternative Preview Methods

### Command Line Demo
For a terminal-based demonstration:
```bash
python cli.py --demo
```

### Python Examples
For programmatic usage examples:
```bash
python examples.py
```

### Interactive Python
For hands-on exploration:
```bash
python
>>> from appeal_system import *
>>> # Create services and explore...
```

## 🔍 What to Look For

### Agent Experience
- ✅ AI suggestions are contextual and helpful
- ✅ Success probability changes based on content
- ✅ Tone recommendations adapt to situation
- ✅ Form validation prevents incomplete submissions

### Supervisor Experience
- ✅ Validity scores reflect appeal quality
- ✅ Priority recommendations are logical
- ✅ Red flags identify potential issues
- ✅ Supporting factors highlight strengths
- ✅ Decision drafts are professional and appropriate

### Technical Quality
- ✅ Clean, modern UI
- ✅ Fast response times
- ✅ No errors in browser console
- ✅ Mobile-friendly design
- ✅ Intuitive user experience

## 🛠️ Troubleshooting

### Server Won't Start
```bash
# Make sure dependencies are installed
pip install -r requirements.txt

# Check if port 5000 is available
lsof -i :5000

# Try a different port
python preview.py --port 8080
```

### Page Not Loading
- Check that the server is running (look for startup message)
- Verify you're using http://localhost:5000 (not https)
- Try refreshing the page (Ctrl+R or Cmd+R)
- Check browser console for errors (F12)

### AI Suggestions Not Appearing
- Make sure you entered text in the initial thoughts field
- Check browser console for errors
- Verify the appeal was created successfully

## 📚 Next Steps

After previewing:
1. **Read the Documentation**
   - `README.md` - Full user guide
   - `ARCHITECTURE.md` - System design
   - `IMPLEMENTATION_SUMMARY.md` - Complete overview

2. **Explore the Code**
   - `appeal_system/` - Core system
   - `preview.py` - Web interface
   - `templates/` - HTML templates

3. **Run the Tests**
   ```bash
   python -m unittest discover tests/
   ```

4. **Try Customization**
   - Modify the HTML templates
   - Adjust AI algorithms
   - Add new features

## 💡 Tips

- The preview uses mock data - perfect for demonstration
- All appeals are stored in memory (reset on server restart)
- Try creating multiple appeals to see the supervisor view populate
- Experiment with different appeal reasons to see AI adapt
- The system is fully functional within the preview

## 🎉 Enjoy Exploring!

The web preview showcases the complete functionality of the Evaluation Appeal System. Take your time to explore both agent and supervisor workflows, and see how AI assistance improves the appeal process at every step.

For questions or issues, check the documentation or open an issue on GitHub.
