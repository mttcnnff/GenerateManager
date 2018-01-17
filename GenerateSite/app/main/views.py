from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm, AddMember
from .. import db
from ..models import MemberModel
from ..decorators import admin_required, permission_required
from flask_login import login_required



@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/members', methods=['GET', 'POST'])
def members():
    form = AddMember()
    members = MemberModel.query.all()
    if form.validate_on_submit():
        new_member = MemberModel(name=form.name.data, email=form.email.data)
        db.session.add(new_member)
        db.session.commit()
        return redirect(url_for('main.members'))
    return render_template('members.html', form=form, members=members)

@main.route('/ang', methods=['GET'])
def angular():
    return render_template('index1.html')
