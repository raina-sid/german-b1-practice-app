# 🇩🇪 German Prep — Telc B1 Exam Practice App

A practice app designed to hack the Telc B1 German exam. Built for immigrants in Germany who want to pass the B1 exam efficiently with 1 hour of daily study.

## Quick Start

```bash
# Activate virtual environment
source venv/bin/activate

# Run the app
python app.py

# Open in browser
open http://localhost:5000
```

## Features

- **🧩 Sprachbausteine Trainer** — 74 grammar exercises across 8 pattern types (connectors, prepositions, verb position, Konjunktiv II, adjective endings, relative pronouns, collocations, tenses)
- **📊 Dashboard** — Track your progress, streaks, XP, and study phase
- **🎵 Focus Music** — Built-in lo-fi / classical / rain music player
- **🏆 Achievements & Easter Eggs** — Stay motivated with hidden surprises
- **📈 Adaptive Learning** — Wrong answers re-enter the queue for retry

## Easter Eggs 🤫

- Click the logo 5 times for a German tongue twister
- Try the Konami code (↑↑↓↓←→←→BA)
- Visit `/geheim` for motivation
- Get 10 in a row for a surprise
- Study after 11 PM or before 6 AM for special badges

## 12-Week Study Plan

The app follows a structured 12-week plan with 3 exam readiness checkpoints:
- **Weeks 1-3**: Grammar Foundation + Sprachbausteine
- **Week 4**: Grammar Consolidation
- **Weeks 5-6**: Reading + Listening
- **Week 7**: Writing + Speaking
- **Week 8**: First Mock Exam → *Checkpoint 1*
- **Weeks 9-10**: Targeted Drilling + Second Mock → *Checkpoint 2*
- **Weeks 11-12**: Final Polish + Third Mock → *Checkpoint 3*

## Tech Stack

- Python 3 + Flask
- SQLite (via SQLAlchemy)
- Tailwind CSS + Alpine.js (via CDN)
- No build step required
