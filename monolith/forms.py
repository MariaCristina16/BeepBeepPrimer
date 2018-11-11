from flask_wtf import FlaskForm
from wtforms import Form, RadioField, SubmitField, validators
import wtforms as f
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = f.StringField('Email', validators=[DataRequired()])
    password = f.PasswordField('Password', validators=[DataRequired()])
    display = ['email', 'password']


class UserForm(FlaskForm):
    email = f.StringField('Email', validators=[DataRequired()])
    firstname = f.StringField('Firstname')
    lastname = f.StringField('Lastname')
    password = f.PasswordField('Password')
    age = f.IntegerField('Age')
    weight = f.FloatField('Weight')
    max_hr = f.IntegerField('Max_hr')
    rest_hr = f.IntegerField('Rest_hr')
    vo2max = f.FloatField('Vo2max')

    display = ['email', 'firstname', 'lastname', 'password',
               'age', 'weight', 'max_hr', 'rest_hr', 'vo2max']


class DeleteForm(FlaskForm):
    password = f.PasswordField('Password', validators=[DataRequired()])
    display = ['password']


class ObjectiveForm(FlaskForm):
    name = f.StringField('Name', validators=[DataRequired()])
    start_date = f.DateField('Start date', validators=[DataRequired()])
    end_date = f.DateField('End Date', validators=[DataRequired()])
    target_distance = f.FloatField('Target Distance', validators=[DataRequired()])

    display = ['name', 'start_date', 'end_date', 'target_distance']

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        result = True

        # Check start_date < end_date
        if self.start_date.data > self.end_date.data:
            result = False

        return result


class MailForm(FlaskForm):
    setting_mail = RadioField('setting', choices=[('6', '6 hours'), ('12', '12 hours'), ('24','24 hours')])
    display = ['setting']
    #setting = RadioField('setting', choices=['6 hours','12 hours','24 hours'])