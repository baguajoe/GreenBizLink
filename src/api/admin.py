  
import os
from flask_admin import Admin
from .models import db, User
from flask_admin.contrib.sqla import ModelView
from api.models import db, User, Interest, Company, Connection, FavoriteConnect

def setup_admin(app):
    admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

    # Add models to the admin interface
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Interest, db.session))
    admin.add_view(ModelView(Company, db.session))
    admin.add_view(ModelView(Connection, db.session))
    admin.add_view(ModelView(FavoriteConnect, db.session))


    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))