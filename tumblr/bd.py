from tumblr import app, database
from tumblr.models import User, Posts

with app.app_context():
    database.create_all()
