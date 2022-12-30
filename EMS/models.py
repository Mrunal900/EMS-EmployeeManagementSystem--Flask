from EMS import db, login_manager
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(60))
    phone = db.Column(db.String(20))
    department = db.Column(db.String(50))
    role = db.Column(db.String(50))
    salary = db.Column(db.String(50))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "{}".format(self.name)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


