import json
import random
from datetime import datetime, date, timedelta
from pathlib import Path

from flask import Flask, render_template, jsonify, request
from config import Config
from models import db, UserProgress, StudySession, DailyActivity, Achievement, UserSettings

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

DATA_DIR = Path(__file__).parent / "data"


def load_json(filename):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


def load_all_exercises():
    """Load exercises from all sprachbausteine JSON files."""
    exercises = []
    for f in sorted(DATA_DIR.glob("sprachbausteine*.json")):
        with open(f, "r", encoding="utf-8") as fh:
            exercises.extend(json.load(fh))
    return exercises


def get_or_create_settings():
    settings = UserSettings.query.first()
    if not settings:
        settings = UserSettings(start_date=date.today())
        db.session.add(settings)
        db.session.commit()
    return settings


def get_streak():
    """Calculate current study streak."""
    today = date.today()
    streak = 0
    check_date = today
    while True:
        activity = DailyActivity.query.filter_by(date=check_date).first()
        if activity and activity.exercises_completed > 0:
            streak += 1
            check_date -= timedelta(days=1)
        else:
            if check_date == today:
                # Today hasn't started yet, check from yesterday
                check_date -= timedelta(days=1)
                continue
            break
    return streak


def get_streak_emoji(streak):
    if streak == 0:
        return "🌱"
    elif streak < 3:
        return "🌱"
    elif streak < 7:
        return "🔥"
    elif streak < 14:
        return "🔥🔥"
    elif streak < 30:
        return "⚡"
    else:
        return "🏆"


def get_level_info(xp):
    levels = [
        (0, "Anfänger", "Beginner"),
        (100, "Lernende/r", "Learner"),
        (300, "Fortgeschritten", "Intermediate"),
        (600, "Experte", "Expert"),
        (1000, "Meister", "Master"),
    ]
    current_level = levels[0]
    next_level = levels[1] if len(levels) > 1 else None
    for i, (threshold, name_de, name_en) in enumerate(levels):
        if xp >= threshold:
            current_level = (threshold, name_de, name_en)
            next_level = levels[i + 1] if i + 1 < len(levels) else None
        else:
            break
    progress = 0
    if next_level:
        range_total = next_level[0] - current_level[0]
        range_done = xp - current_level[0]
        progress = int((range_done / range_total) * 100) if range_total > 0 else 100
    else:
        progress = 100
    return {
        "level_name_de": current_level[1],
        "level_name_en": current_level[2],
        "xp": xp,
        "progress": progress,
        "next_level_xp": next_level[0] if next_level else None,
    }


def get_current_week(settings):
    if not settings.start_date:
        return 1
    days_elapsed = (date.today() - settings.start_date).days
    return min(max(days_elapsed // 7 + 1, 1), 12)


def get_phase_info(week):
    phases = {
        (1, 3): ("Grammar Foundation + Sprachbausteine", "Grammatik-Grundlagen", "40 min Sprachbausteine / 20 min Lesen", "sprachbausteine"),
        (4, 4): ("Grammar Consolidation", "Grammatik-Festigung", "30 min mixed Sprachbausteine / 30 min Übungen", "sprachbausteine"),
        (5, 6): ("Reading + Listening Intensive", "Lesen + Hören", "30 min Lesen / 30 min Hören", "reading"),
        (7, 7): ("Writing + Speaking", "Schreiben + Sprechen", "30 min Schreiben / 30 min Sprechen", "writing"),
        (8, 8): ("First Mock Exam", "Erste Probeprüfung", "Mixed practice + Mock exam", "mock"),
        (9, 9): ("Targeted Weak Spot Drilling", "Schwachstellen-Training", "45 min weak areas / 15 min review", "drill"),
        (10, 10): ("Second Mock Exam", "Zweite Probeprüfung", "Drilling + Mock exam", "mock"),
        (11, 11): ("Deep Review", "Tiefe Wiederholung", "15 min each: Sprachbausteine, Lesen, Schreiben, Sprechen", "review"),
        (12, 12): ("Final Polish + Confidence", "Endspurt! 🏁", "Final mock + light review", "final"),
    }
    for (start, end), info in phases.items():
        if start <= week <= end:
            return {
                "name_en": info[0],
                "name_de": info[1],
                "daily_routine": info[2],
                "primary_module": info[3],
            }
    return {"name_en": "Study Time", "name_de": "Lernzeit", "daily_routine": "Mixed practice", "primary_module": "sprachbausteine"}


def get_module_stats(module):
    total = UserProgress.query.filter_by(module=module).count()
    correct = UserProgress.query.filter_by(module=module, is_correct=True).count()
    accuracy = int((correct / total) * 100) if total > 0 else 0
    return {"total": total, "correct": correct, "accuracy": accuracy}


# ─── Routes ────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    settings = get_or_create_settings()
    week = get_current_week(settings)
    phase = get_phase_info(week)
    streak = get_streak()
    level = get_level_info(settings.xp)
    fun_facts = load_json("fun_facts.json")
    fun_fact = random.choice(fun_facts)

    # Days until exam
    days_until_exam = None
    if settings.exam_date:
        days_until_exam = (settings.exam_date - date.today()).days

    # Module stats
    sb_stats = get_module_stats("sprachbausteine")

    # Today's activity
    today_activity = DailyActivity.query.filter_by(date=date.today()).first()

    # Weak areas analysis (grammar types with < 65% accuracy and at least 5 attempts)
    weak_areas = []
    if sb_stats["total"] > 0:
        type_stats = db.session.query(
            UserProgress.exercise_type,
            db.func.count(UserProgress.id).label('total'),
            db.func.sum(db.case((UserProgress.is_correct == True, 1), else_=0)).label('correct')
        ).filter(
            UserProgress.module == "sprachbausteine"
        ).group_by(
            UserProgress.exercise_type
        ).having(
            db.func.count(UserProgress.id) >= 5
        ).all()

        for type_name, total, correct in type_stats:
            accuracy = int((correct / total) * 100) if total > 0 else 0
            if accuracy < 65:
                # Get friendly label
                type_labels = {
                    "connector": "Konnektoren",
                    "preposition": "Präpositionen",
                    "verb_position": "Wortstellung",
                    "konjunktiv": "Konjunktiv II",
                    "adjective_ending": "Adjektivendungen",
                    "relative_pronoun": "Relativsätze",
                    "collocation": "Feste Wendungen",
                    "tense": "Zeitformen",
                    "passive": "Passiv",
                    "negation": "Verneinung",
                }
                weak_areas.append({
                    "type": type_name,
                    "label": type_labels.get(type_name, type_name),
                    "accuracy": accuracy,
                    "total": total
                })
        
        # Sort by accuracy (worst first)
        weak_areas.sort(key=lambda x: x["accuracy"])

    # Time greeting
    hour = datetime.now().hour
    if hour < 6:
        greeting = "Noch wach? 🦉"
    elif hour < 12:
        greeting = "Guten Morgen!"
    elif hour < 18:
        greeting = "Guten Tag!"
    elif hour < 22:
        greeting = "Guten Abend!"
    else:
        greeting = "Nachtschicht? Respekt! 🦉"

    return render_template(
        "dashboard.html",
        greeting=greeting,
        week=week,
        phase=phase,
        streak=streak,
        streak_emoji=get_streak_emoji(streak),
        level=level,
        fun_fact=fun_fact,
        days_until_exam=days_until_exam,
        exam_date=settings.exam_date,
        sb_stats=sb_stats,
        today_activity=today_activity,
        weak_areas=weak_areas,
    )


@app.route("/sprachbausteine")
def sprachbausteine():
    return render_template("sprachbausteine.html")


@app.route("/writing")
def writing():
    prompts = load_json("writing_prompts.json")
    return render_template("writing.html", prompts=prompts)


@app.route("/speaking")
def speaking():
    data = load_json("speaking_topics.json")
    return render_template("speaking.html", data=data)


@app.route("/vocabulary")
def vocabulary():
    data = load_json("vocabulary.json")
    return render_template("vocabulary.html", data=data)


@app.route("/geheim")
def geheim():
    return render_template("geheim.html")


# ─── API ──────────────────────────────────────────────────────────

@app.route("/api/exercises")
def api_exercises():
    """Get exercises, optionally filtered by type and week."""
    exercise_type = request.args.get("type", "all")
    week = request.args.get("week", None, type=int)
    difficulty = request.args.get("difficulty", None, type=int)
    limit = request.args.get("limit", 20, type=int)
    exclude = request.args.get("exclude", "")

    exercises = load_all_exercises()

    if exercise_type != "all":
        exercises = [e for e in exercises if e["type"] == exercise_type]
    if week:
        exercises = [e for e in exercises if e.get("week", 1) <= week]
    if difficulty:
        exercises = [e for e in exercises if e.get("difficulty", 1) <= difficulty]
    if exclude:
        exclude_set = {x for x in exclude.split(",") if x}
        if exclude_set:
            exercises = [e for e in exercises if str(e.get("id")) not in exclude_set]

    # Shuffle and limit
    random.shuffle(exercises)
    exercises = exercises[:limit]

    return jsonify(exercises)


@app.route("/api/answer", methods=["POST"])
def api_answer():
    """Submit an answer and record progress."""
    data = request.get_json()
    exercise_id = data.get("exercise_id")
    selected = data.get("selected_index")
    correct_index = data.get("correct_index")
    exercise_type = data.get("exercise_type", "unknown")

    is_correct = selected == correct_index

    # Record progress
    progress = UserProgress(
        exercise_id=exercise_id,
        module="sprachbausteine",
        exercise_type=exercise_type,
        is_correct=is_correct,
    )
    db.session.add(progress)

    # Update daily activity
    today = date.today()
    activity = DailyActivity.query.filter_by(date=today).first()
    if not activity:
        activity = DailyActivity(date=today, exercises_completed=0, correct_answers=0, minutes_studied=0)
        db.session.add(activity)
    activity.exercises_completed = (activity.exercises_completed or 0) + 1
    if is_correct:
        activity.correct_answers = (activity.correct_answers or 0) + 1

    # Update XP
    settings = get_or_create_settings()
    if is_correct:
        settings.xp += 10
    else:
        settings.xp += 2  # Still get something for trying

    db.session.commit()

    # Check for achievements
    achievements = check_achievements(settings)

    return jsonify({
        "correct": is_correct,
        "xp_gained": 10 if is_correct else 2,
        "total_xp": settings.xp,
        "new_achievements": achievements,
    })


@app.route("/api/vocab/export")
def api_vocab_export():
    """Export vocabulary as TSV for Anki import."""
    data = load_json("vocabulary.json")
    lines = ["#separator:tab", "#html:false", "#tags column:3"]
    for cat in data["categories"]:
        tag = cat["name_en"].replace(" & ", "_").replace(" ", "_")
        for word in cat["words"]:
            front = word["de"]
            back = f"{word['en']}\\n{word['ex']}"
            lines.append(f"{front}\t{back}\t{tag}")
    content = "\n".join(lines)
    from flask import Response
    return Response(
        content,
        mimetype="text/tab-separated-values",
        headers={"Content-Disposition": "attachment;filename=b1_vocab_anki.txt"}
    )


@app.route("/api/progress")
def api_progress():
    """Get overall progress stats."""
    settings = get_or_create_settings()
    streak = get_streak()
    level = get_level_info(settings.xp)

    # Per-type stats
    type_stats = {}
    exercises = load_all_exercises()
    types = set(e["type"] for e in exercises)
    for t in types:
        total = UserProgress.query.filter_by(module="sprachbausteine", exercise_type=t).count()
        correct = UserProgress.query.filter_by(module="sprachbausteine", exercise_type=t, is_correct=True).count()
        type_stats[t] = {
            "total": total,
            "correct": correct,
            "accuracy": int((correct / total) * 100) if total > 0 else 0,
        }

    return jsonify({
        "streak": streak,
        "level": level,
        "type_stats": type_stats,
    })


@app.route("/api/settings", methods=["POST"])
def api_settings():
    """Update user settings."""
    data = request.get_json()
    settings = get_or_create_settings()
    if "exam_date" in data and data["exam_date"]:
        settings.exam_date = datetime.strptime(data["exam_date"], "%Y-%m-%d").date()
    if "start_date" in data and data["start_date"]:
        settings.start_date = datetime.strptime(data["start_date"], "%Y-%m-%d").date()
    db.session.commit()
    return jsonify({"status": "ok"})


@app.route("/api/achievements")
def api_achievements():
    """Get all unlocked achievements."""
    achievements = Achievement.query.all()
    return jsonify([{
        "id": a.achievement_id,
        "name": a.name,
        "description": a.description,
        "unlocked_at": a.unlocked_at.isoformat(),
    } for a in achievements])


def check_achievements(settings):
    """Check and unlock new achievements."""
    new_achievements = []

    achievement_checks = [
        ("first_blood", "Erste Schritte! 🐣", "Completed your first exercise", lambda: UserProgress.query.count() >= 1),
        ("ten_streak", "Zehn am Stück! 🔥", "Got 10 correct in a row (this session counts across all time)", lambda: _check_correct_streak(10)),
        ("century", "Hundert! 💯", "Completed 100 exercises", lambda: UserProgress.query.count() >= 100),
        ("night_owl", "Nachteule 🦉", "Studied after 11 PM", lambda: datetime.now().hour >= 23),
        ("early_bird", "Früher Vogel 🐦", "Studied before 6 AM", lambda: datetime.now().hour < 6),
        ("grammar_nerd", "Grammatik-Nerd 🤓", "Got 50 Sprachbausteine correct", lambda: UserProgress.query.filter_by(module="sprachbausteine", is_correct=True).count() >= 50),
        ("connector_master", "Konnektor-Meister 🔗", "Got 20 connector exercises correct", lambda: UserProgress.query.filter_by(exercise_type="connector", is_correct=True).count() >= 20),
        ("xp_500", "Halber Tausender 🌟", "Earned 500 XP", lambda: settings.xp >= 500),
    ]

    for aid, name, desc, check_fn in achievement_checks:
        existing = Achievement.query.filter_by(achievement_id=aid).first()
        if not existing and check_fn():
            achievement = Achievement(achievement_id=aid, name=name, description=desc)
            db.session.add(achievement)
            new_achievements.append({"id": aid, "name": name, "description": desc})

    if new_achievements:
        db.session.commit()

    return new_achievements


def _check_correct_streak(n):
    """Check if the last N answers were all correct."""
    recent = (
        UserProgress.query
        .order_by(UserProgress.answered_at.desc())
        .limit(n)
        .all()
    )
    return len(recent) >= n and all(r.is_correct for r in recent)


# ─── Init ─────────────────────────────────────────────────────────

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
