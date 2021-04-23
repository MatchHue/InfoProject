from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()



class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(120), nullable=False)

  def toDict(self):
    return{
      "id": self.id,
      "username": self.username,
      "password": self.password
    }

  def set_password(self, password):
    self.password = generate_password_hash(password, method='sha256')

  def check_password(self, password):
    return check_password_hash(self.password, password)

  def __repr__(self):
    return '<User {}>'.format(self.username)


class Route(db.Model):
  id=db.Column(db.Integer,primary_key=True)
  start=db.Column(db.String(100))
  destination=db.Column(db.String(100))
  travel_time=db.Column(db.Integer())
  traffic=db.Column(db.String(100))
  

  def toDict(self):
    return{
      "id": self.id,
      "start": self.start,
      "destination": self.destination,
      "travel_time":self.travel_time,
      "traffic": self.traffic
    }
