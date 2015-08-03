from flask import Flask
from ircb.config import settings
from ircb.models import get_session, create_tables

app = Flask(__name__)


if __name__ == '__main__':
    create_tables()
    session = get_session(settings.DB_URI)
    app.run()
