# Quick Start Guide

## Preview the Project in 3 Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Web Preview

```bash
python preview.py
```

### 3. Open Your Browser

Visit http://localhost:5000 and explore:

- **Home Page**: System overview and statistics
- **Agent View**: Create an appeal with AI assistance
- **Supervisor View**: Triage and decide on appeals

## What You'll See

### Agent Experience 🤖

1. View your evaluation details
2. Enter initial thoughts about why you're appealing
3. Get AI-powered suggestions:
   - Success probability estimate
   - Key points to include
   - Tone recommendations
4. Refine your appeal with evidence
5. Submit for review

### Supervisor Experience 👔

1. View dashboard with statistics
2. See all pending appeals with AI analysis:
   - Validity score (0-100%)
   - Priority recommendations
   - Key points and red flags
   - Review time estimates
3. Get AI-generated decision drafts
4. Make quick decisions (approve/reject/request more info)

## Alternative: Command Line Demo

For a terminal-based demonstration:

```bash
python cli.py --demo
```

Or run comprehensive examples:

```bash
python examples.py
```

## What's Next?

After previewing, check out:
- `README.md` - Full documentation
- `ARCHITECTURE.md` - System design details
- `IMPLEMENTATION_SUMMARY.md` - Complete overview
- `tests/` - Run tests with: `python -m unittest discover tests/`
