from flask import render_template, url_for, flash, redirect,request,abort,jsonify,session
import requests
import json
import imaplib
from THAT import application,db,bcrypt #using bcrypt to has the passwords in user database
from THAT.models import User, Lecture
from THAT.forms import RegistrationForm, LoginForm,LectureForm,SearchForm

from flask_login import login_user,current_user,logout_user,login_required
from sqlalchemy.orm.exc import NoResultFound

from datetime import datetime, timedelta
from random import sample
from THAT.search import KMPSearch

import urllib.request
import urllib.parse
from flask_mail import Message


#everything here that begins with @ is a decorator
@application.route("/")
@application.route("/home")
def home():
    return render_template('home.html',db=db,User=User,Lecture=Lecture)


@application.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    lectures=Lecture.query.filter_by(user_id=current_user.id).all()
    lectures.reverse()
    form1=SearchForm()
    if form1.validate_on_submit():
        arr=[] 
        lectures2=[]
        for lecture in lectures:
            a=form1.search.data
            b=lecture.title
            if KMPSearch(a.casefold(),b.casefold()):
                arr.append(lecture.id)
                lectures2.append(Lecture.query.filter_by(id=lecture.id).first())
        if len(arr)==0:
            flash('Lecture not found!','warning')
            return redirect(url_for('dashboard'))
        else:
            data=json.dumps(form1.search.data)
            return render_template('search_lecture.html', title='Searched Lecture', lectures2=lectures2,data=data)
    return render_template('dashboard.html', title='Dashboard', lectures=lectures,form1=form1,form2=form2)
    

@application.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard')) #redirects user to dashboard if already logged in; function name is passed in url_for
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8') #returns hashed password, decode converts it from byte to string
        #if app_password field is not-empty
        user=User(username=form.username.data,email=form.email.data,password=hashed_password)

        db.session.add(user)
        db.session.commit()
        flash(f'You are almost there.', 'success')
        return render_template("dashboard.html",pn=user.mobileNum)
    return render_template('register.html', title='Register', form=form)

@application.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))  
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')#looks for queries in request; args is a dictionary; we use get and not directly use 'next' as key to return the value because key might be empty leading to an error. get, in that case would fetch a none
            flash('Greetings '+form.username.data+'!','success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@application.route("/logout")
def logout():
    logout_user()
    flash('You have logged out  !','success')
    return redirect(url_for('home'))

@application.route("/account")
@login_required
def account():
    return render_template('account.html',title='Account')



@application.route("/account/delete",methods=['GET', 'POST'])
@login_required
def delete_account():
    user=User.query.filter_by(id=current_user.id).first()
    lectures=Lecture.query.filter_by(user_id=current_user.id).all()
    for lecture in lectures:
        db.session.delete(lecture)
    connection=Connection.query.filter_by(user_a_id=current_user.id).all()
    for c in connection:
        db.session.delete(c)
    connection=Connection.query.filter_by(user_b_id=current_user.id).all()
    for c in connection:
        db.session.delete(c)
    db.session.commit()
    db.session.delete(user)
    db.session.commit()
    flash('Account deleted','success')
    return redirect(url_for('home'))

@application.route("/lecture/new",methods=['GET', 'POST'])
@login_required
def new_lecture():
    form=LectureForm()
    if form.validate_on_submit():
        lecture1=Lecture(title=form.title.data,date=form.date.data,starttime=form.starttime.data, endtime=form.endtime.data,details=form.details.data,remindtime=form.remindtime.data,status=form.status.data,user_id=current_user.id)
        db.session.add(lecture1)
        db.session.commit()               
        flash('Lecture scheduled!','success')
        return redirect(url_for('dashboard'))
    return render_template('schedule_lecture.html',title='New Lecture',form=form, legend='Schedule Lecture')


@application.route("/lecture/ <int:lecture_id>")
@login_required
def lecture(lecture_id):
    lecture=Lecture.query.get_or_404(lecture_id) #get_or_404 returns the requested page if it exists else it returns a 404 error
    return render_template('lecture.html',title=lecture.title,lecture=lecture)

@application.route("/lecture/ <int:lecture_id>/update",methods=['GET', 'POST'])
@login_required
def update_lecture(lecture_id):
    lecture=Lecture.query.get_or_404(lecture_id)
    if lecture.user_id!=current_user.id:  # this is optional since we display only a prticular user's lectures in his dashboard
        abort(403)
    form=LectureForm()
    if form.validate_on_submit():
        lecture.title = form.title.data
        lecture.details = form.details.data
        lecture.date=form.date.data
        lecture.starttime=form.starttime.data
        lecture.endtime=form.endtime.data
        lecture.status=form.status.data
        db.session.commit()
        flash('Lecture updated!', 'success')
        return redirect(url_for('lecture',lecture_id=lecture.id))
    elif request.method == 'GET':
        form.title.data = lecture.title
        form.details.data = lecture.details
        form.date.data=lecture.date
        form.starttime.data=lecture.starttime
        form.endtime.data=lecture.endtime
        form.status.data=lecture.status
    return render_template('schedule_lecture.html', title='Update Lecture',form=form, legend='Update Lecture')

@application.route("/lecture/ <int:lecture_id>/delete",methods=['GET', 'POST'])

@login_required
def delete_lecture(lecture_id):
    lecture=Lecture.query.get_or_404(lecture_id)
    if lecture.user_id!=current_user.id:  # this is optional since we display only a prticular user's lectures in his dashboard
        abort(403)
    db.session.delete(lecture)
    db.session.commit()
    flash('Lecture deleted!','warning')
    return redirect(url_for('dashboard'))





