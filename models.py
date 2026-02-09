from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserProgress(db.Model):
    """Tracks every answer the user gives."""

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.String(50), nullable=False)
    module = db.Column(db.String(50), nullable=False)  # sprachbausteine, reading, etc.
    exercise_type = db.Column(db.String(50), nullable=False)  # connector, preposition, etc.
    is_correct = db.Column(db.Boolean, nullable=False)
    answered_at = db.Column(db.DateTime, default=datetime.utcnow)


class StudySession(db.Model):
    """Tracks study sessions."""

    id = db.Column(db.Integer, primary_key=True)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime, nullable=True)
    module = db.Column(db.String(50))
    total_questions = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)


class DailyActivity(db.Model):
    """Tracks daily study activity for streak calculation."""

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, default=date.today)
    minutes_studied = db.Column(db.Integer, default=0)
    exercises_completed = db.Column(db.Integer, default=0)
    correct_answers = db.Column(db.Integer, default=0)


class Achievement(db.Model):
    """Tracks unlocked achievements / easter eggs."""

    id = db.Column(db.Integer, primary_key=True)
    achievement_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    unlocked_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserSettings(db.Model):
    """User preferences and exam configuration."""

    id = db.Column(db.Integer, primary_key=True)
    exam_date = db.Column(db.Date, nullable=True)
    start_date = db.Column(db.Date, default=date.today)
    daily_goal_minutes = db.Column(db.Integer, default=60)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
