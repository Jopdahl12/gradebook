from flask import render_template, flash, redirect, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from .forms import LoginForm
from .models import Student, Course, Admin


@app.route('/', methods=['GET','POST'])
@app.route('/login', methods= ['GET','POST'])
def login():
	# if g.user is not None and g.user.is_authenticated():
	# 	return redirect('/home')
	form = LoginForm()
	if form.validate_on_submit():
		login_user(form.user, form.remember_me.data)
		session['user_id']=form.user.id
		session['remember_me']=form.remember_me.data
		if form.user in Student.query.all():
			return redirect('/student/%s' % form.user.id)
		else:
			return redirect('/admin/%s' % form.user.id)
	return render_template('login.html', title='login', form= form) #, providers=app.config['OPENID_PROVIDERS'])

@login_manager.user_loader
def load_user(id):
	user=Student.query.get(str(id))
	if user is None:
		user=Admin.query.get(str(id))
	return user

@app.route('/student/<id>')
@login_required
def stud_home(id):
	user = Student.query.filter_by(id=id).first()

	return render_template('student_home.html', user=user)

@app.route('/admin/<id>')
@login_required
def admin_home(id):
	user = Admin.query.filter_by(id=id).first()

	return render_template('admin_home.html', user=user)

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/')

@app.route('/home')
@login_required
def home():
	user = currennt_user
	if user in Student.query.all():
		return redirect('/student/%s' % user.id)
	return redirect('/admin/%s' % user.id)

@app.route('/profile')
@login_required
def profile():
	user = current_user
	if user in Admin.query.all():
		return redirect('/admin/%s/profile' % user.id)
	else:
		return redirect('/student/%s/profile' % user.id)

@app.route('/student/<id>/profile')
@login_required
def show_stud_prof(id):
	user = Student.query.filter_by(id=id).first()
	return render_template('student_profile.html', user=user)

@app.route('/admin/<id>/profile')
@login_required
def show_admin_prof(id):
	user = Admin.query.filter_by(id=id).first()
	return render_template('admin_profile.html', user=user)















