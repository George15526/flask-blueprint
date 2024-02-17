from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from . import db
from .models import Users
from .__init__ import set_password, check_password

auth = Blueprint('auth', __name__,)

@auth.route('/<username>', methods=['GET', 'POST'])
def index(username):
    return render_template('index.html', username=username)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        
        if request.values.get("login_submit") == 'login':
            login_username = request.form['username']
            login_password = request.form['password']
            
            user = Users.query.filter_by(username = login_username).first()
            
            if check_password(user, login_password):
                session['username'] = login_username
                flash('Login Success', 'success')
                return redirect(url_for('auth.index', username=login_username))
            else:
                flash('Login Failed, Please Check.', 'danger')
    return render_template('login.html')

@auth.route('/logout')
def logout():
    return render_template('login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        
        if request.values.get("register_submit") == 'register':
        
            username = request.form['username']
            gender = request.form['gender']
            email = request.form['email']
            password = request.form['password']
            check_password = request.form['check_password']
            
            if check_password == password:
                
                new_user = Users(username=username, 
                                gender=gender,
                                email=email,
                                password_hashed=set_password(password))
                
                db.session.add(new_user)
                db.session.commit()
                
                flash('Signup Success! Please Login.', 'success')
                
                return redirect(url_for('auth.login'))
            
            else:
                flash('Two password are not the same, please check!')
                
        
    return render_template('register.html')

@auth.route('/manage', methods=['GET', 'POST'])
def manage():
    query = Users.query.all()
        
    return render_template('manage.html', query=query)

@auth.route('/delete_datas', methods=['GET', 'POST'])
def delete_datas():
    if request.method == 'POST':
        users = request.form.getlist("row_check")
        for i in users:
            user_id = int(i)
            delete_user = Users.query.filter_by(id=user_id).first()
            db.session.delete(delete_user)
            db.session.commit()
        
        if request.values.get("check_all") == "delete_all":
            delete_users = Users.query.all()
        
            for delete_user in delete_users:
                db.session.delete(delete_user)
                db.session.commit()
          
    return redirect(url_for('auth.manage'))