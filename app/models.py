from app import db, g
import random

class Classroom(db.Model):
	__tablename__ = 'classroom'
	student_id = db.Column(db.String(8), db.ForeignKey('student.id'), primary_key=True)
	course_name = db.Column(db.String(80), db.ForeignKey('course.name'), primary_key=True)
	overall_grade = db.Column(db.String(1))
	possible = db.Column(db.Integer, default=0)
	grade = db.Column(db.Float, default=0)
	total_points = db.Column(db.Integer, default=0)
	course = db.relationship("Course", backref="stud_ass")
	assignments = db.relationship("Assignment", backref='for_class')


	def update_possible(self):
		self.possible=0
		for assignment in self.assignments:
			self.possible+=assignment.out_of
		return self

	def update_grade(self):
		self.total_points = 0
		for assignment in self.assignments:
			self.total_points+=assignment.total
		if self.possible == 0:
			self.grade = 0
			return self
		self.grade = self.total_points/self.possible
		return self

	def update_overall_grade(self):
		if self.grade >= .90:
			self.overall_grade='A'
		elif self.grade >= .80:
			self.overall_grade='B'
		elif self.grade >= .70:
			self.overall_grade='C'
		elif self.grade >= .60:
			self.overall_grade='D'
		else: 
			self.overall_grade='F'
		return self

	def remove(self, ass):
		assignment = Assignment.query.filter_by(name=ass, student_id=self.student_id).first()
		if assignment in self.assignments:
			self.assignments.remove(assignment)
		return self

	def is_empty(self):
		if self.assignments is None or self.assignments == []:
			return True
		return False


	def __repr__(self):
		return (self.student.first_name + self.student.last_name + ' ' + self.course.name)

class Student(db.Model):
	id = db.Column(db.String(8), primary_key=True)
	first_name = db.Column(db.String(50), index=True)
	last_name = db.Column(db.String(50), index=True)
	GPA = db.Column(db.Float)
	year = db.Column(db.Integer)
	total_credits = db.Column(db.Integer)
	student_pass = db.Column(db.String(50))
	classes = db.relationship('Classroom', backref='student')

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)  # python 3

	def check_password(self, password):
		if self.student_pass == password:
			return True
		return False

	def register(self, coursename):
			c = Classroom.query.filter_by(course_name=coursename).all()
			classroom = Classroom(student_id=self.id, course_name=coursename)
			if c is not None and c != []:
				for assignment in c[0].assignments:
					key = random.randint(0,1000)
					while key in g:
						key = random.randint(0,1000)
					g.append(key)
					a = Assignment(id=key, name=assignment.name, out_of=assignment.out_of, student_id=classroom.student_id)
					db.session.add(a)
					classroom.assignments.append(a)
					db.session.add(classroom)
					classroom.update_possible()
					db.session.add(classroom)
				db.session.commit()
			self.classes.append(classroom)
			return self

	def drop(self, coursename):
			classroom = Classroom.query.filter_by(student_id=self.id, course_name=coursename).first()
			self.classes.remove(classroom)
			db.session.delete(classroom)
			return self

	def set_password(self, newpass):
		self.student_pass = newpass
		return self

	def __repr__(self):
		return (self.first_name + ' ' + self.last_name)

class Admin(db.Model):
	id = db.Column(db.String(8), primary_key=True)
	first_name = db.Column(db.String(50), index=True)
	last_name = db.Column(db.String(50), index=True)
	admin_pass = db.Column(db.String(50))
	position = db.Column(db.String(50))
	email = db.Column(db.String(120))
	begin = db.Column(db.String(5))
	end = db.Column(db.String(5))
	classes = db.relationship("Course", backref="teacher", lazy='dynamic')

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)  # python 2
		except NameError:
			return str(self.id)  # python 3

	def check_password(self, password):
		if self.admin_pass == password:
			return True
		return False

	def set_office_hours(self, begin, end):
		self.begin=begin
		self.end=end
		return self

	def set_email(self, email=''):
		if self.email==None:
			self.email = self.id + '@gradetracker.com'
		else:
			self.email = email
		return self

	def set_password(self, newpass):
		self.admin_pass = newpass
		return self

	def __repr__(self):
		return (self.first_name + ' ' + self.last_name)

class Course(db.Model):
	course_num = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), index=True, unique=True)
	admin_id = db.Column(db.String(8), db.ForeignKey('admin.id'))

	def __repr__(self):
		return self.name

class Assignment(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), index=True)
	total = db.Column(db.Integer, default=0)
	out_of = db.Column(db.Integer, default=0)
	student_id = db.Column(db.String(8), db.ForeignKey('classroom.student_id'))
	score = db.Column(db.Float, default=0.0)
	letter = db.Column(db.String(2), default='NA')


	def set_score(self):
		if self.out_of is None or self.total is None:
			self.score = 0.0
			self.total = 0
		else:
			self.score = self.total/self.out_of
		if self.score >= .90:
			self.letter='A'
		elif self.score >= .80:
			self.letter='B'
		elif self.score >= .70:
			self.letter='C'
		elif self.score >= .60:
			self.letter='D'
		else: 
			self.letter='F'
		return self

	def __repr__(self):
		return self.name







