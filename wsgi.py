import sys
import os

# Only modify path if we're on PythonAnywhere
if 'PYTHONANYWHERE_SITE' in os.environ:
    path = '/home/yourusername/mysite'
    if path not in sys.path:
        sys.path.append(path)

from app import app as application
application.secret_key = 'your-secret-key'  # Add this for session support 