# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 13:12:28 2020

@author: Aruna
"""

# -*- coding: utf-8 -*-
"""


"""
import os
from flask import Flask, flash, redirect, render_template, request, session, abort

from flask import Flask, render_template, redirect, url_for, session, request
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, current_user, login_user, \
                        login_required, logout_user

# from flask_session import Session

import faceLoginApp 
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired



# app = Flask(__name__, static_url_path='', static_folder='static')
# app.config['SECRET_KEY'] = 'secret!'
# app.config['SESSION_TYPE'] = 'filesystem'
# login = LoginManager(app)
# Session(app)
app = Flask(__name__)

socketio = SocketIO(app)
recognizer = faceLoginApp.UserLogin

# class User(UserMixin, object):
#     def __init__(self, id=None, name=''):
#         self.id = id
#         self.name = name

# @login.user_loader
# def load_user(id):
#     try:
#       name = session['user_' + id]
#       return User(id, name)
#     except:
#       return None
class UserRegistryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class User(db.Entity, UserMixin):
    login = Required(str, unique=True)
    username = Required(str)
    password = Required(str)
    is_active = Required(bool)
    recipes = Set("faceData")

"""" register and login both on first page"""
@db_session
@app.route('/userRegistry', methods=['GET', 'POST'])
def user_registry():
    form = UserRegistryForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            email = request.form['email']
            password = hash_password(request.form['password'])
            name = request.form['name']
            exist = User.get(login=email)
            if exist:
                flash('The address %s is already in use, choose another one' % email)
                return redirect('/userRegistry')
            curr_user = User(login=email, username=name, password=password, is_active=False)
            commit()
            localhost_url = 'http://0.0.0.0:5000'
            message = Mail(
                from_email='<sender_email>',
                to_emails=To(email),
                subject='Confirm your account',
                html_content='<h2>Hello,<h2> to complete your registration click  <a href="' + (
                        os.environ.get("HEROKU_URL") or localhost_url) + '/activate/' + str(
                    curr_user.id) + '"> here </a>.'
            )
            try:
                sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
                response = sg.send(message)
            except Exception as e:
                print e.message
            return redirect('/')
    else:
        return render_template('registry_form.html', title='Register', form=form)
  
@app.route('/')
def home():
        if not session.get('logged_in'):
            ###register template here when clicked will go to route to capture pic and get login credentia
            flash('Face login')
            ret=recognizer.captureAndCompare('Aruna')
    # if ret==1:
    #     flash("Welcome to MEFY")
    
        if ret==1:
            return("Welcome to MEFY")
        else:

            return render_template('login.html')
    # else:
    #     return "Hello Boss!"
@app.route('/login', methods=['POST'])
def do_admin_login():
     if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return("Successfully logged in using credentials")
     else:
            flash('Register')
            return render_template('register.html')
            
            ####ask user to register cuz no database found
    # return home()

        
    # # else:
    # elif (request.form['password'] == '123' and request.form['username'] == 'user1'):
    #         ###match with userdatabase///create userpassword database also
    #         session['logged_in'] = True
    # else:
            
            

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
 
# @app.route('/register')
# def register():
    
#     return render_template('register.html')

# # @app.route('/'
# # def index():
# #     if form.validate_on_submit():
# #         if 'Register' in request.form:
# #             pass # do something
# #         elif 'Already registered? Face Login' in request.form:
# #             pass # do something else

# @app.route('/login', methods=['POST','GET'])
# def login():
#     # print("heree")
#     # if current_user.is_authenticated:
#     #     return redirect(url_for('register'))
#     #if request.method == 'POST':
#     ret=recognizer.captureAndCompare('Aruna') ###not displaying print statements
#     print(ret)  
#         # return(ret)
#     if ret==1:
#         return("Welcome!! You are successfully logged in")
#        # print(request.form)
#     # if request.form['auth_key'] == '1234567890':
#     #         login_user(User(1, 'Aruna'))
#     #         session['user_1'] = 'Aruna'
#     #         return redirect(url_for('login'))
#     else:
#             return render_template('login.html')
# #################Add login username and password page
   

# @app.route('/logout')
# @login_required
# def logout():
#     print('Logging out')
#     logout_user()
#     return redirect(url_for('index'))

# @socketio.on('stream')
# def send_image(img):
#     print("here")
    
       

# # real time streaming
# @socketio.on('stream-end')
# def send_image_end(img):
#   emit('stream-end', {'endded': True}, broadcast=True)

# @socketio.on('verify-user')
# def verifyt_user(img):
#   id, name, accouracy = recognizer.Recognize()
#   auth_key = ''
#   if id is not None:
#       auth_key = '1234567890'
#   emit('verify-user', {'id': id, 'name': name, 'auth_key': auth_key,'accouracy': accouracy}, broadcast=True)

# @socketio.on('connect')
# def test_connect():
#     emit('my response', {'data': 'Connected'})

# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')

# if __name__ == '__main__':
    
#     socketio.run(app, debug=True)
    #app.run()

