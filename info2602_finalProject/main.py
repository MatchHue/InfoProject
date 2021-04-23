import json
from flask_cors import CORS
from flask import Flask, request, render_template, redirect, flash, url_for, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, current_user, login_user, login_required,logout_user

from models import db, User, Route
from forms import LogIn


login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  CORS(app)
  login_manager.init_app(app)
  db.init_app(app)
  return app

app = create_app()

app.app_context().push()




@app.route('/', methods=['GET'])
def login_index():
  form = LogIn()
  return render_template('login.html', form=form)


@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): 
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): 
        flash('Logged in successfully.') 
        login_user(user) 
        return redirect(url_for('index')) 
  flash('Invalid credentials')
  return redirect(url_for('login_index'))


@app.route('/routes')
@login_required
def index():
  routes=Route.query.all()
  return render_template('app.html',routes=routes)

@app.route('/insertRoute',methods=['POST'])
def insert_action():
  data=request.form
  newRoute=Route(start=data['start'],destination=data['destination'],travel_time=data['travel_time'],traffic=data['traffic'])
  db.session.add(newRoute)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/deleteRoute/<id>',methods=['GET'])
def delete_action(id):
  data=request.get_json()
  route=Route.query.get(id)
  db.session.delete(route)
  db.session.commit()
  return redirect(url_for('index'))

@app.route('/searchRoute',methods=['GET'])
def search_route():
  loc=request.args.get('search')
  route=list(Route.query.filter_by(start=loc))
  destination=list(Route.query.filter_by(destination=loc))
  routes=route+destination
  return render_template('app.html',routes=routes)

@app.route('/shareRoute/<id>',methods=['GET'])
def share_route(id):
  data=request.get_json()
  route=Route.query.get(id)
  return json.dumps(route.toDict())

  
@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  flash('Logged Out!')
  return redirect(url_for('login_index'))   

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)