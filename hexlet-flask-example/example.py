from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash, get_flashed_messages
import json


# Это callable WSGI-приложение
app = Flask(__name__)
app.secret_key = "secret_key"


def validate(user):
    errors = {}
    if not user['name']:
        errors['name'] = "Can't be blank"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors


@app.route('/')
def hello_world():
    return 'Hello, Hexlet!'


@app.route('/users/<int:id>')
def get_user(id):
    f = open('hexlet-flask-example/users.json')
    users = json.load(f)
    f.close()

    user = {}
    for current_user in users:
        if current_user['id'] == id:
            user = current_user

    return render_template(
        'users/show.html',
        user=user,
    )


@app.route('/users/<int:id>/edit')
def edit_user(id):
    f = open('hexlet-flask-example/users.json')
    users = json.load(f)
    f.close()

    user = {}
    for current_user in users:
        if current_user['id'] == id:
            user = current_user

    errors = {}

    return render_template(
        'users/edit.html',
        user=user,
        errors=errors,
    )


@app.route('/users/new')
def users_new():
    user = {'name': '', 'email': ''}
    errors = {}
    return render_template(
        'users/new.html',
        user=user,
        errors=errors,
    )


@app.get('/users/')
def get_users():
    messages = get_flashed_messages(with_categories=True)
    f = open('hexlet-flask-example/users.json')
    users = json.load(f)
    f.close()

    term = request.args.get('term', '')
    filter_users = [user for user in users if str(term) in user['name']]
    return render_template(
            'users/users.html',
            messages=messages,
            filter_users=filter_users,
        )


@app.post('/users/')
def users_post():
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template(
            'users/new.html',
            user=user,
            errors=errors,
        ), 422

    f = open('hexlet-flask-example/users.json')
    users = json.load(f)
    f.close()

    user['id'] = max((user.get('id', 0) for user in users), default=0) + 1
    users.append(user)

    f = open('hexlet-flask-example/users.json', 'w')
    json.dump(users, f, indent=2)
    f.close()

    flash('User was added successfully', 'success')

    return redirect(url_for('get_users'), code=302)


@app.post('/users/<int:id>/patch')
def patch_user(id):
    user = request.form.to_dict()
    errors = validate(user)
    if errors:
        return render_template(
            'users/edit.html',
            user=user,
            errors=errors,
        ), 422

    f = open('hexlet-flask-example/users.json')
    users = json.load(f)
    f.close()

    for current_user in users:
        if current_user['id'] == id:
            current_user['name'] = user['name']
            current_user['email'] = user['email']

    f = open('hexlet-flask-example/users.json', 'w')
    json.dump(users, f, indent=2)
    f.close()

    flash('User was updated successfully', 'success')

    return redirect(url_for('get_users'), code=302)


@app.post('/users/<int:id>/delete')
def delete_user(id):
    f = open('hexlet-flask-example/users.json')
    users = json.load(f)
    f.close()

    user = {}
    for current_user in users:
        if current_user['id'] == id:
            user = current_user

    users.remove(user)
    f = open('hexlet-flask-example/users.json', 'w')
    json.dump(users, f, indent=2)
    f.close()

    flash('User has been deleted', 'success')

    return redirect(url_for('get_users'), code=302)
