from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os
from .utils import create_serializer
from flask_mail import Mail

load_dotenv()

app = Flask(__name__)
app.config.from_object("config.Config")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = os.getenv("secretKey")

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Initialize URLSafeTimedSerializer
s = create_serializer(app.config["SECRET_KEY"])

# Initialize extensions
mail = Mail(app)

# Import your routes
from App import routes  # noqa: E402, F401 #! Don't remove this line!
