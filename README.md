<div align="center">

# 🇩🇪 German B1 Practice App

### Fast-track your *telc Deutsch B1* exam – not the language itself.

A hacker-style desktop web app for **daily, focused drills** across all B1 sections with gamified XP, streaks, and Anki-ready flashcards.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/raina-sid/german-b1-practice-app.git
cd german-b1-practice-app

# Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open in browser
open http://localhost:5000
```

---

## ✨ Features

### 🧩 **Sprachbausteine Trainer**
- **156 exercises** across 10 grammar types
- Adaptive difficulty with instant feedback
- Session persistence (resume where you left off)
- Type filters to drill weak areas
- Review mode for mistakes
- Keyboard shortcuts (1-4 to answer, Enter to continue, Esc to dashboard)

### 📝 **Vocabulary Builder**
- **140 B1 words** organized by exam topics
- Flashcard mode with example sentences
- **Anki TSV export** for spaced repetition
- Mark difficult words for review

### ✍️ **Writing Practice**
- **20 email prompts** (invitation, complaint, inquiry, apology, declining)
- Redemittel (useful phrases) for each type
- Word counter & timer
- Self-check checklist

### 🗣️ **Speaking Practice**
- **20 Teil 2 topics** (present a topic)
- **15 Teil 3 scenarios** (plan with partner)
- Redemittel for all 3 speaking parts
- Practice timer

### 📊 **Progress Tracking**
- XP system with levels
- Daily streak counter
- Weak areas analysis (< 65% accuracy)
- Per-type accuracy breakdown
- 12-week study plan with checkpoints

### 🎵 **Focus Features**
- Built-in music player (lo-fi, classical, rain, silence)
- Dark mode only (easier on eyes)
- Achievements & Easter eggs
- Mobile-responsive with hamburger menu

---

## 📚 Content Inventory

| Module | Content | Notes |
|--------|---------|-------|
| **Sprachbausteine** | 156 exercises | 10 grammar types, adaptive review |
| **Vocabulary** | 140 words | 9 categories, Anki export |
| **Writing** | 20 prompts | Email templates + Redemittel |
| **Speaking** | 35 scenarios | Topics + planning + Redemittel |
| **Reading** | ❌ None | Use your book or telc PDFs |
| **Listening** | ❌ None | Use Hueber audio or telc PDFs |

---

## 🎯 12-Week Study Plan

The app guides you through a structured plan with early-exit checkpoints:

| Weeks | Focus | Daily Routine | Checkpoint |
|-------|-------|---------------|------------|
| 1-3 | Grammar Foundation | 40 min Sprachbausteine / 20 min Reading | - |
| 4 | Consolidation | 30 min mixed drills / 30 min exercises | - |
| 5-6 | Reading + Listening | 30 min Reading / 30 min Listening | - |
| 7 | Writing + Speaking | 30 min Writing / 30 min Speaking | - |
| 8 | First Mock Exam | Practice test + weak spot drilling | **70%+ → go for exam** |
| 9 | Targeted Drilling | 45 min weak areas / 15 min review | - |
| 10 | Second Mock Exam | Practice test + drilling | **65%+ → comfortable pass** |
| 11-12 | Final Polish | Full mocks + light review | **Maximum confidence** |

---

## 🚧 What This App Does NOT Cover

⚠️ **Important:** This app covers ~40% of the exam. You **must** supplement with:

- **📖 Reading practice** → Use "Fit fürs Zertifikat" book or [free telc PDFs](https://www.telc.net/pruefungsteilnehmende/sprachpruefungen/pruefungen/detail/telc-deutsch-b1.html)
- **🎧 Listening practice** → Use Hueber audio files or telc audio
- **📝 Full mock exams** → Download free telc Modelltest or buy "Mit Erfolg zu telc Deutsch B1 Testbuch"
- **🗣️ Speaking partner** → Find on italki, Tandem app, or local meetups
- **✍️ Writing feedback** → Get corrections from a tutor or language exchange

**Success formula:**
```
This App (40%) + Official Tests (30%) + Book/Audio (20%) + Speaking Partner (10%) = Pass B1
```

---

## 🤫 Easter Eggs

- Click the logo 5 times → German tongue twister
- Konami code (↑↑↓↓←→←→BA) → Bratwurst achievement
- Visit `/geheim` → Motivational page
- 10 correct in a row → Confetti celebration
- Study after 11 PM or before 6 AM → Night owl / Early bird badges

---

## 🛠️ Tech Stack

- **Backend:** Python 3 + Flask
- **Database:** SQLite (via Flask-SQLAlchemy)
- **Frontend:** Tailwind CSS + Alpine.js (via CDN)
- **No build step required** — just run and go

---

## 📖 Usage Tips

### **Daily Routine (1 hour)**
1. Check dashboard for weak areas
2. Do 30 Sprachbausteine (filtered by weak type)
3. Review mistakes once
4. 20 min reading/listening from external sources
5. Track progress on dashboard

### **Keyboard Shortcuts (Sprachbausteine)**
- `1` `2` `3` `4` — Select answer
- `Enter` or `Space` — Next question
- `Esc` — Return to dashboard

### **Session Management**
- Sessions auto-save to localStorage
- Resume where you left off if you navigate away
- Choose session size (10/20/30/50) before starting
- Filter by grammar type for targeted practice

---

## 🤝 Contributing

Found a bug? Want to add more exercises? Open an issue or PR!

---

## ⚖️ License

MIT License — do whatever you want with this code.

---

## 🎓 Disclaimer

This app is a **study tool**, not a complete course. It's designed to complement official exam materials, not replace them. For best results, combine with:
- Official telc practice tests
- Your textbook (e.g., "Fit fürs Zertifikat")
- Speaking practice with native speakers
- Professional tutoring (if needed)

---

<div align="center">

**Viel Erfolg beim B1! 🚀**

Made with ☕ for immigrants in Germany

</div>
