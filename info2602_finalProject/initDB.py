from main import app
from models import db, User, Route
import json

db.create_all(app=app)
with open('data.json') as routes:
  data=json.load(routes)
  bob=User(username="bob")
  bob.set_password("bobpass")
  db.session.add(bob)
  for row in data:
    route=Route(start=row['start'],destination=row['destination'],travel_time=row['travel_time'],traffic=row['traffic'])
    db.session.add(route)
  db.session.commit()


print('database initialized!')