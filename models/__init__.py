from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .norm import Norm
from .case import Case