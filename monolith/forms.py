from flask_wtf import FlaskForm
from wtforms import RadioField
import wtforms as f
from wtforms.validators import DataRequired, NumberRange, Email


class LoginForm(FlaskForm):
    email = f.StringField('Email', validators=[DataRequired("Insert a valid email."), Email()])
    password = f.PasswordField('Password', validators=[DataRequired("Insert your password")])

    display = ['email', 'password']


class UserForm(FlaskForm):
    email = f.StringField('Email', validators=[DataRequired("Insert a valid email."), Email()])
    firstname = f.StringField('Firstname', validators=[DataRequired("Insert your first name.")])
    lastname = f.StringField('Lastname', validators=[DataRequired("Insert your last name")])
    password = f.PasswordField('Password', validators=[DataRequired("Insert a valid password")])
    age = f.IntegerField('Age', validators=[NumberRange(min=0)])
    weight = f.FloatField('Weight')
    max_hr = f.IntegerField('Max_hr')
    rest_hr = f.IntegerField('Rest_hr')
    vo2max = f.FloatField('Vo2max')

    display = ['email', 'firstname', 'lastname', 'password',
               'age', 'weight', 'max_hr', 'rest_hr', 'vo2max']


class DeleteForm(FlaskForm):
    password = f.PasswordField('Password', validators=[DataRequired("Insert a valid password")])
    display = ['password']


class ObjectiveForm(FlaskForm):
    name = f.StringField('Name', validators=[DataRequired("Insert the objective name")])
    start_date = f.DateField('Start date', format='%Y-%m-%d', validators=[DataRequired("Insert when to start the objective")])
    end_date = f.DateField('End Date', format='%Y-%m-%d', validators=[DataRequired("Insert when to end the objective")])
    target_distance = f.FloatField('Target Distance', validators=[DataRequired("Insert the target distance")])

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
    setting_mail = f.RadioField('setting', choices=[('6', '6 hours'), ('12', '12 hours'), ('24','24 hours')])
    display = ['setting']

class ChallengeForm(FlaskForm):
    run_one = f.IntegerField('run_one', validators=[DataRequired()])
    run_two = f.IntegerField('run_two', validators=[DataRequired()])
    display = ['run_one','run_two']