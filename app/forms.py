from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
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