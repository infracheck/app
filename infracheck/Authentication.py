import hashlib

import flask_login

from infracheck import login_manager

# TODO: Replace with database
users = {'martin': {'password': hashlib.sha3_512(b"pw").hexdigest()}}


class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user
