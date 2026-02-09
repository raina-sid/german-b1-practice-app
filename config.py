import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "deutsch-b1-hacker-geheim")
    SQLALCHEMY_DATABASE_URI = "sqlite:///deutsch.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
