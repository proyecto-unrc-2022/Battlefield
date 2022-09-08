from app import db

from ..models.user import User

from bcrypt import hashpw, gensalt, checkpw

def add_user(username, password, email):
  encoded_pass = hash_password(password.encode('UTF-8'))
  user = User(username=username, password=encoded_pass, email=email)
  db.session.add(user)
  db.session.commit()

def hash_password(plaintext_password):
    return hashpw(plaintext_password, gensalt())

def check_password(plaintext_password, hashed_password):
    return checkpw(plaintext_password, hashed_password)

