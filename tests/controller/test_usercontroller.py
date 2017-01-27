import pytest
from flask import url_for
from har import app, db
from har.model import user

@pytest.fixture
def setup():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'secretkey'
    db.create_all()

    yield

    db.drop_all()

@pytest.fixture
def create_user():
    user_id = user.create_user('email', 'password')

    yield user_id

def test_login(setup, create_user):
    test_app = app.test_client()
    response = test_app.post('/login', data={
        'email': 'email',
        'password': 'password'
    })

    test_user = user.get_user_by_id(create_user)
    assert response.status_code == 302
    assert test_user.is_authenticated
    assert test_user.last_login

def test_login_failed(setup, create_user):
    test_app = app.test_client()
    response = test_app.post('/login', data={
        'email': 'asd',
        'password': 'asd'
    })

    assert response.status_code == 302

def test_unauthorized_access(setup):
    test_app = app.test_client()
    response = test_app.get('log')

    assert response.status_code == 302
