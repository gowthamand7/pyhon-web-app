from flask import Flask, render_template, request, session, jsonify

from src.common.database import Database
from src.models.users import User

app = Flask(__name__)
app.secret_key = 'gowthaman'


@app.route('/')
def helloworld():
    return render_template('login.html')


@app.before_first_request
def initDB():
    Database.initialize()


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/auth/login',methods=['POST'])
def loginValidate():
    email = request.form['email']
    password = request.form['password']

    if User.loginValid(email,password):
        User.login(email)
    else:
        return jsonify(error='Invalid user name or password, Please try to login again')

    return render_template('profile.html',email=session['email'])


@app.route('/auth/register',methods=['POST'])
def registerNewUser():
    email = request.form['email']
    password = request.form['password']
    if User.register(email,password) is not False:
        return render_template('profile.html', email=session['email'])
    else:
        return 'User already present in the App, Please login'


if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False)