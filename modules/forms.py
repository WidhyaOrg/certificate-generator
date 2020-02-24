from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

class ValidationForm(Form):
	email = TextField('Please enter your Email-ID', validators=[validators.DataRequired()])
