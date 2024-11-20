import os


class Config:
    SECRET_KEY = os.getenv("secretKey", "your-default-secret-key")
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.example.com")
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "your-email@example.com")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your-email-password")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
