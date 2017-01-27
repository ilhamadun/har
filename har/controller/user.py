"""Controller for request to /user URLs"""

from datetime import datetime
from flask import request, abort, render_template
from flask_login import login_user, logout_user
from har.model.user import get_user_by_email, authenticate, update_last_login
from .url import redirect_back

def login():
    """Attempt to log user in"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if authenticate(email, password):
            user = get_user_by_email(email)
            login_user(user)
            update_last_login(user)

        return redirect_back()

    else:
        return render_template('login.html')

def logout():
    """Log user out."""
    logout_user()
    return redirect_back()
