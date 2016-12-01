from wtforms import Form, StringField, IntegerField, validators

class RegistrationForm(Form):
	first_name = StringField('First name', [validators.Length(min=4, max=52)])
	last_name = StringField('Last name', [validators.Length(min=4, max=52)])
	email = StringField('E-mail address', [validators.Length(min=6, max=36)])
	id = StringField('Id', [validators.Length(min=10, max=10)])
	age = IntegerField('Age', [validators.required()])