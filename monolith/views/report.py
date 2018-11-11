from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from monolith.forms import MailForm
from monolith.database import db, Report

report = Blueprint('report', __name__)


# In this we specify the setting for the management of the report
@report.route('/settingreport', methods=['GET', 'POST'])
@login_required
def settingreport():
    form = MailForm()
    if request.method == 'POST':
            current_report = db.session.query(Report).filter(Report.runner_id == current_user.id).first()
            if current_report is None:
                print('Qua')
                new_report = Report()
                new_report.set_user(current_user.id)
                new_report.set_timestamp()
                option = request.form['setting_mail']
                new_report.set_decision(option)
                db.session.add(new_report)
                db.session.commit()
                flash('Settings updated', category='success')
            else:
                current_report.set_timestamp()
                option = request.form['setting_mail']
                current_report.set_decision(option)
                db.session.merge(current_report)
                db.session.commit()
                flash('Settings updated', category='success')
    return render_template('mail.html', form=form)
