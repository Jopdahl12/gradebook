from app import db

class Student(db.Model):
	id = db.Column(db.String(8), primary_key=True)
	first_name = db.Column(db.String(50), index=True)
	last_name = db.Column(db.String(50), index=True)
	GPA = db.Column(db.Float)
	year = db.Column(db.Integer)
	total_credits = db.Column(db.Integer)
	student_pass = db.Column(db.String(50))
	classes = db.relationship("Course", backref="student",lazy='dynamic')

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
	student_id = db.Column(db.String(8), db.ForeignKey('student.id'))
	admin_id = db.Column(db.String(8), db.ForeignKey('admin.id'))
	# assignments = db.relationship("Assignment", backref="course", lazy='dynamic')

	def __repr__(self):
		return self.name

# class Assignment(db.Model):
# 	assign_num = db.Column(db.Integer, primary_key=True)
# 	name = db.Column(db.String(100), index=True)
# 	total = db.Column(db.Float)
# 	out_of = db.Column(db.Integer)
# 	score = db.Column(db.Float)
# 	course = db.Column(db.Integer, db.ForeignKey('course.course_num'))

# 	def copmute_score(self):
# 		score = self.total/self.out_of
# 		return score

# 	def __repr__(self):
# 		return self.name





