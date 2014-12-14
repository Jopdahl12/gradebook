from flask import render_template, flash, redirect, session
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager
from .forms import LoginForm
from .models import Student, Course, Admin, Classroom, Assignment


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

@app.route('/about')
def about():
	return render_template('about.html',
							title='About GradeTracker')

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
	user = current_user
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
	return render_template('stud_profile.html', user=user)

@app.route('/admin/<id>/profile')
@login_required
def show_admin_prof(id):
	user = Admin.query.filter_by(id=id).first()
	return render_template('admin_profile.html', user=user)

@app.route('/student/<id>/<course_name>')
@login_required
def student_classpage(id, course_name):
	user=current_user
	course=Course.query.filter_by(name=course_name).first()
	classroom = Classroom.query.filter_by(course_name=course_name).first()
	assignments=True
	if classroom.is_empty():
		assignments=False
	return render_template('classpageStud.html',
							course=course,
							classroom=classroom,
							user=user,
							assignments=assignments)

@app.route('/admin/<id>/<course_name>')
@login_required
def admin_classpage(id, course_name):
	user=current_user
	course=Course.query.filter_by(name=course_name).first()
	classrooms=Classroom.query.filter_by(course_name=course_name).all()
	students=[]
	ids=[]
	for classroom in classrooms:
		ids.append(classroom.student_id)
	for id in ids:
		students.append(Student.query.filter_by(id=id).first())
	return render_template('classpageAdmin.html',
							students=students,
							course=course,
							user=user)

@app.route('/register')
@login_required
def reg():
	user = current_user
	courses = Course.query.all()
	classrooms = Classroom.query.all()
	taking=[]
	for course in user.classes:
		for classroom in classrooms:
			if course == classroom:
				taking.append(course.course_name)
	return render_template('register.html', 
							courses=courses, 
							classrooms=classrooms,
							user=user,
							taking=taking)

@app.route('/drop')
@login_required
def dr():
	user = current_user
	return render_template('drop.html',
							user=user)
@app.route('/register/<class_name>')
@login_required
def register(class_name):
	user = current_user
	user = user.register(class_name)
	db.session.add(user)
	db.session.commit()
	return redirect('/register')

@app.route('/drop/<class_name>')
@login_required
def drop(class_name):
	user = current_user
	classroom = Classroom.query.filter_by(student_id=user.id, course_name=class_name)
	user = user.drop(class_name)
	db.session.add(user)
	db.session.commit()
	return redirect('/drop')

@app.route('/student/<id>/courses')
@login_required
def student_courses(id):
	user = current_user 
	courses=[]
	for thing in user.classes:
		for c in Course.query.all():
			if thing.course_name == c.name:
				courses.append(c)

	return render_template('student_classes.html',
							courses=courses,
							user=user)

@app.route('/admin/<id>/courses')
@login_required
def admin_courses(id):
	user = current_user
	return render_template('admin_classes.html',
							user=user)

@app.route('/student/<id>/contacts')
@login_required
def studentContact(id):
	user = current_user
	admins = Admin.query.all()
	return render_template('stud_contact.html',
							admins=admins,
							user=user)

@app.route('/admin/<id>/contacts')
@login_required
def adminContact(id):
	user = current_user
	admins = Admin.query.all()
	return render_template('admin_contact.html',
							admins=admins,
							user=user)










