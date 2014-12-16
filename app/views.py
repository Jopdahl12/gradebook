from flask import render_template, flash, redirect, session, request
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, login_manager, g
from .forms import LoginForm, ChangePassword, ChangeMail, AddAssignment
from .models import Student, Course, Admin, Classroom, Assignment
import random

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
	classrooms = Classroom.query.filter_by(course_name=course_name).all()
	classroom = Classroom.query.filter_by(course_name=course_name, student_id=id).first()
	# if classroom.is_empty() == False:
	# 	for assignment in classrooms[0].assignments:
	# 		if assignment not in classroom.assignments:
	# 			key = generate_key()
	# 			a=Assignment(id=key, name=assignment.name, out_of=assignment.out_of, student=user.id)
	# 			db.session.add(a)
	# 			a.score()
	# 			db.session.add(a)
	# 			classroom.assignments.append(a)
	# 			db.session.add(classroom)
	# 			classroom.update_possible()
	# 			db.session.add(classroom)
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
	classrooms = course.stud_ass
	students=[]
	ids=[]
	for classroom in classrooms:
		ids.append(classroom.student_id)
	for id in ids:
		students.append(Student.query.filter_by(id=id).first())
	assignments =[]
	if classrooms !=[] and classrooms is not None: 
		assignments = classrooms[0].assignments
	return render_template('classpageAdmin.html',
							students=students,
							course=course,
							user=user,
							classrooms=classrooms,
							assignments=assignments)

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
	print (Classroom.query.filter_by(course_name=class_name).all())
	user = user.register(class_name)
	db.session.add(user)
	db.session.commit()
	return redirect('/register')

@app.route('/drop/<class_name>')
@login_required
def drop(class_name):
	user = current_user
	classroom = Classroom.query.filter_by(student_id=user.id, course_name=class_name).first()
	for assignment in classroom.assignments:
		classroom.assignments.remove(assignment)
		db.session.delete(assignment)
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

@app.route('/student/<id>/changepassword', methods=['GET', 'POST'])
@login_required
def student_changePassword(id):
	user = current_user
	form = ChangePassword()
	if form.validate_on_submit():
		if form.id.data != user.id:
			form.id.errors = list(form.id.errors)
			form.id.errors.append('This is not you')
			return render_template('student_changePassword.html',
									user=user,
									form=form)
		user.student_pass = form.password
		db.session.add(user)
		db.session.commit()
		return redirect('/profile')
	return render_template('student_changePassword.html',
							user=user,
							form=form)


@app.route('/admin/<id>/changepassword', methods=['GET', 'POST'])
@login_required
def admin_changePassword(id):
	user = current_user
	form = ChangePassword()
	if form.validate_on_submit():
		if form.id.data != user.id:
			form.id.errors = list(form.id.errors)
			form.id.errors.append('This is not you')
			return render_template('admin_changePassword.html',
									user=user,
									form=form)
		user.admin_pass = form.password
		db.session.add(user)
		db.session.commit()
		return redirect('/profile')
	return render_template('admin_changePassword.html',
							user=user,
							form=form)

@app.route('/changemail')
@login_required
def changeMail():
	user=current_user
	return redirect('/admin/{{user.id}}/changemail')

@app.route('/admin/<id>/changemail', methods=['GET','POST'])
@login_required
def admin_changeMail(id):
	user=current_user
	form = ChangeMail()
	if form.validate_on_submit():
		user.email=form.newEmail.data
		db.session.add(user)
		db.session.commit()
		return redirect('/admin/%s/profile' % user.id)
	return render_template('admin_changemail.html',
							user=user,
							form=form)

@app.route('/admin/<id>/<course_name>/add', methods=['GET','POST'])
@login_required
def add(id, course_name):
	user=current_user
	course = Course.query.filter_by(name=course_name).first()
	classrooms = Classroom.query.filter_by(course_name=course_name).all()
	for classroom in classrooms:
		print (classroom.student_id, classroom.course_name, classroom.assignments)
	students=[]
	ids=[]
	if classrooms != [] and classrooms is not None:
		assignments=classrooms[0].assignments
		classroom = classrooms[0]
	else:
		assignments =[]
		classroom = None
	for classroom in classrooms:
		ids.append(classroom.student_id)
	for id in ids:
		students.append(Student.query.filter_by(id=id).first())


	form = AddAssignment()
	pass_=1
	if form.validate_on_submit():
		for classroom in classrooms:
			key=generate_key()
			print (pass_, classroom.student_id, classroom.course_name)
			a=Assignment(id=key, name=form.name, out_of=form.out_of, for_class=classroom, student_id=classroom.student_id)
			db.session.add(a)
			a.set_score()
			db.session.add(a)
			db.session.add(classroom)
			classroom = a.for_class.update_possible()
			print (classroom.assignments)
			db.session.add(classroom)
			pass_+=1
		db.session.commit()
		return redirect('/admin/{0}/{1}'.format(user.id, course_name))
	return render_template('addassignment.html',
							user=user,
							course=course,
							classrooms=classrooms,
							form=form,
							students=students,
							assignments=assignments,
							classroom=classroom)

@app.route('/admin/<id>/<course_name>/delete', methods=['GET','POST'])
@login_required
def delete(id, course_name):
	user = current_user
	course = Course.query.filter_by(name=course_name).first()
	classrooms = Classroom.query.filter_by(course_name=course_name).all()
	students=[]
	ids=[]
	for classroom in classrooms:
		ids.append(classroom.student_id)
	for id in ids:
		students.append(Student.query.filter_by(id=id).first())
	return render_template('delete.html',
							user=user,
							classrooms=classrooms,
							course=course,
							students=students)

@app.route('/<course_name>/delete', methods=['GET','POST'])
@login_required
def handle_delete(course_name):
	request.path='/templates/delete'
	user=current_user
	course = Course.query.filter_by(name=course_name)
	classrooms = Classroom.query.filter_by(course_name=course_name).all()
	for classroom in classrooms:
		print (classroom.possible)
	form = request.form
	for f in form.keys():
		if form[f] == 'on':
			assignments = Assignment.query.filter_by(name=f).all()
			for assignment in assignments:
				for classroom in classrooms:
					key = assignment.id
					reuse_key(key)
					classroom = classroom.remove(assignment.name)
					db.session.add(classroom)
					classroom = classroom.update_possible()
					db.session.add(classroom)
					classroom = classroom.update_grade()
					db.session.add(classroom)
					classroom = classroom.update_overall_grade()
					db.session.add(classroom)
				db.session.delete(assignment)

	db.session.commit()
	return redirect('/admin/{0}/{1}'.format(user.id, course_name))




@app.route('/admin/<id>/<course_name>/<student_id>')
@login_required
def adminview_student(id, course_name,student_id):
	user=current_user
	course = Course.query.filter_by(name=course_name).first()
	student = Student.query.filter_by(id=student_id).first()
	classroom = Classroom.query.filter_by(student_id=student_id, course_name=course_name).first()
	return render_template('admin_student_page.html',
							course=course,
							classroom=classroom,
							user=user,
							assignments=classroom.assignments,
							student=student)


@app.route('/admin/<id>/<course_name>/<student_id>/grade', methods=['GET','POST'])
@login_required
def grade(id, course_name, student_id):
	user=current_user
	course = Course.query.filter_by(name=course_name).first()
	student = Student.query.filter_by(id=student_id).first()
	classroom=Classroom.query.filter_by(student_id=student_id, course_name=course_name).first()
	return render_template('/edit_grade.html',
							user=user,
							student=student,
							classroom=classroom,
							course=course)

@app.route('/<course_name>/<student_id>/grade', methods=['GET','POST'])
@login_required
def handle_grade(course_name, student_id):
	request.path = '/templates/edit_grade'
	user = current_user
	course = Course.query.filter_by(name=course_name).first()
	classroom = Classroom.query.filter_by(course_name=course_name, student_id=student_id).first()
	form = request.form
	for f in form.keys():
		print (form[f])
		if form[f]:
			for assignment in classroom.assignments:
				if assignment.name == f:
					assignment.total = int(form[f])
					db.session.add(assignment)
					assignment.set_score()
					db.session.add(assignment)
					classroom.update_grade()
					db.session.add(classroom)
					classroom.update_overall_grade()
					db.session.add(classroom)
	db.session.commit()
	return redirect('/admin/{0}/{1}'.format(user.id, course_name))

def generate_key():
	key = random.randint(0,1000)
	while key in g:
		key = random.randint(0,1000)
	g.append(key)
	return key

def reuse_key(key):
	if key in g:
		g.pop(g.index(key))


