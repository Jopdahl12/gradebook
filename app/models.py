from app import db

classroom = db.Table('classroom',
	db.Column("student", db.String(8), db.ForeignKey('student.id')),
	db.Column("course", db.Integer, db.ForeignKey('course.name'))
)

class Student(db.Model):
	id = db.Column(db.String(8), primary_key=True)
	first_name = db.Column(db.String(50), index=True)
	last_name = db.Column(db.String(50), index=True)
	GPA = db.Column(db.Float)
	year = db.Column(db.Integer)
	total_credits = db.Column(db.Integer)
	student_pass = db.Column(db.String(50))
	classes = db.relationship("Course",
							secondary= classroom,
							primaryjoin=(classroom.c.student == id),
							backref=db.backref("students", lazy='dynamic'),
							lazy='dynamic')

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
		if not self.is_registered(coursename):
			course = Course.query.filter_by(name=coursename).first()

			self.classes.append(course)
			return self

	def drop(self, coursename):
		if self.is_registered(coursename):
			course = Course.query.filter_by(name=coursename).first()
			self.classes.remove(course)
			return self

	def is_registered(self, coursename):
		return self.classes.filter(classroom.c.course == coursename).count()>0

	def __repr__(self):
		return (self.first_name + ' ' + self.last_name)

class Admin(db.Model):
	id = db.Column(db.String(8), primary_key=True)
	first_name = db.Column(db.String(50), index=True)
	last_name = db.Column(db.String(50), index=True)
	admin_pass = db.Column(db.String(50))
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

	def __repr__(self):
		return 'Administrator %r' % (self.first_name + ' ' + self.last_name)

class Course(db.Model):
	course_num = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), index=True, unique=True)
	# student_id = db.Column(db.String(8), db.ForeignKey('student.id'))
	admin_id = db.Column(db.String(8), db.ForeignKey('admin.id'))
	assignments = db.relationship("Assignment", backref="for_class", lazy='dynamic')

	def is_empty(self):
		if self.assignments is None:
			return True
		return False

	def __repr__(self):
		return self.name

class Assignment(db.Model):
	assign_num = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), index=True)
	total = db.Column(db.Float)
	out_of = db.Column(db.Integer)
	course = db.Column(db.Integer, db.ForeignKey('course.course_num'))

	def score(self):
		score = self.total/self.out_of
		return score


	def __repr__(self):
		return self.name







