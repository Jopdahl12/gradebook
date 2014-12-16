from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, validators, IntegerField
from wtforms.validators import DataRequired
from app import db, models

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	remember_me = BooleanField('remember_me', default=False)

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.user = None

	def validate(self):
		rv = Form.validate(self)
		if not rv:
			return False

		user = models.Student.query.filter_by(id=self.username.data).first()
		if user is None:
			user = models.Admin.query.filter_by(id=self.username.data).first()

		if user is None:
			self.username.errors.append('Unkown Username')
			return False

		if not user.check_password(self.password.data):
			self.password.errors.append('Invalid Password')
			return False

		self.user = user
		return True

class ChangePassword(Form):
	id = StringField('id', validators=[DataRequired()])
	oldPassword = PasswordField('oldPassword', validators=[DataRequired()])
	newPassword = PasswordField('newPassword', [validators.DataRequired(), validators.EqualTo('confirm')])
	confirm = PasswordField('confirm', validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.password = self.oldPassword.data

	def validate(self):
		user = models.Student.query.filter_by(id=self.id.data).first()
		if user is None:
			user = models.Admin.query.filter_by(id=self.id.data).first()

			if user is None:
				self.id.errors = list(self.id.errors)
				self.id.errors.append('Unkown Username')
				return False

			if user.admin_pass != self.oldPassword.data:
				self.oldPassword.errors = list(self.oldPassword.errors)
				self.oldPassword.errors.append('Incorrect Current Password')
				return False
		else:
			if user is None:
				self.id.errors = list(self.id.errors)
				self.id.errors.append('Unkown Username')
				return False
			if user.student_pass != self.oldPassword.data:
				self.oldPassword.errors = list(self.oldPassword.errors)
				self.oldPassword.errors.append('Incorrect Current Password')
				return False

		if self.newPassword.data != self.confirm.data:
			self.confirm.errors = list(self.confirm.errors)
			self.confirm.errors.append('Passwords do not match')
			return False

		self.password = self.newPassword.data
		return True

class ChangeMail(Form):
	newEmail = StringField('newEmail', validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if '@' in self.newEmail.data:
			return True
		return False

class AddAssignment(Form):
	Name = StringField('name', validators=[DataRequired()])
	total = IntegerField('total', validators=[DataRequired()])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
		self.name = self.Name.data
		self.out_of = self.total.data

	def validate(self):
		return True







