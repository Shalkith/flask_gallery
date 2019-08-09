from flask import Flask, render_template, request,redirect, url_for
import string
import os
from data import get_images,jsonreader,jsonwriter,jsondelete
import flask_login


filepath = os.path.dirname(__file__)


app = Flask(__name__)
key = str(os.urandom(24))
key = 'DSFNGDMQWT9J9ASFNM9AIONC90MC09M'
app.secret_key = key

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {'foo@bar.tld': {'password': 'secret'}, 'paul':{'password':'12345'}, 'michelle':{'password':'12345'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email


    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
            return render_template('login.html')


    email = request.form['email']
    try:

        if request.form['password'] == users[email]['password']:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return redirect(url_for('gallery'))

    except:
        pass
    return 'Bad login  <meta http-equiv="Refresh" content="2; url=/login">'



@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('home'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


######### login goes up here ^
app.debug=True

class BenefitTemplateService(object):

    @staticmethod
    def create(params):
        # some validation here

        params['credit_behavior'] = "none"
        return params


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return '404'
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return '500'
    return render_template('404.html'), 404


@app.route('/')
def home():
    return render_template('home.html')

#@app.route('/signup', methods=['GET', 'POST'])
#def register():
#    return "Signup"



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/mygallery')
def gallery():
    data = jsonreader(filepath)
    newlist = []
    data = data['photos']
    for x in data:
        if x["hidden"] == "False":
            newlist.append(x)
    data = newlist
    return render_template('gallery2.html',data = data)

@app.route('/edit',methods=['GET', 'POST'])
@flask_login.login_required
def edit():
    data = jsonreader(filepath)
    newlist = []
    data = data['photos']
    #return str(data)
    return render_template('edit.html',data = data)

@app.route('/new',methods=['GET', 'POST'])
@flask_login.login_required
def new():
    return render_template('new.html')


@app.route('/process',methods=['GET', 'POST'])
def process():
    if request.method=="POST":
        parameters = request.form.to_dict()
        response = BenefitTemplateService.create(parameters)
        jsonwriter(response,filepath)
        return redirect(url_for('edit'))
    else:
        return 'this is not a post'

@app.route('/upload',methods=['GET', 'POST'])
def upload():
    if request.method=="POST":
        f = request.files['newFile']
        f.save('static/photos/'+f.filename.replace(" ","",99))
        parameters = request.form.to_dict()
        response = BenefitTemplateService.create(parameters)
        del response['credit_behavior']
        response['file'] = f.filename.replace(" ","",99)
        jsonwriter(response,filepath)
        return redirect(url_for('gallery'))
    else:
        return redirect(url_for('home'))

@app.route('/delete',methods=['GET', 'POST'])
def delete():
    if request.method=="POST":
        parameters = request.form.to_dict()
        response = BenefitTemplateService.create(parameters)
        jsondelete(response,filepath)

        return redirect(url_for('edit'))
    else:
        return 'this is not a post'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
