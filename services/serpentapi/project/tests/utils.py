# services/serpentapi/project/tests/utils.py


from project import db
from project.api.models.user import User


def add_user(username, email, password):
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user
