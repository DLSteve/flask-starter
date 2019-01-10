from flask import render_template
from flask_login import login_required
from . import profile


@profile.route('/me')
@login_required
def me():
    return render_template('profile/user_profile.html', title='Home')
