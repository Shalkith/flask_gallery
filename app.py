from flask import Flask, render_template, request,redirect, url_for
import string
import os
from data import get_images,jsonreader,jsonwriter,jsondelete

key = str(os.urandom(24))
app = Flask(__name__)
app.debug=True
app.secret_key = key

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


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    data = jsonreader()
    newlist = []
    data = data['photos']
    for x in data:
        if x["hidden"] == "False":
            newlist.append(x)
    data = newlist
    return render_template('gallery2.html',data = data)

@app.route('/edit',methods=['GET', 'POST'])
def edit():
    data = jsonreader()
    newlist = []
    data = data['photos']
    #return str(data)
    return render_template('edit.html',data = data)

@app.route('/new',methods=['GET', 'POST'])
def new():
    return render_template('new.html')


@app.route('/process',methods=['GET', 'POST'])
def process():
    if request.method=="POST":
        parameters = request.form.to_dict()
        response = BenefitTemplateService.create(parameters)
        jsonwriter(response)
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
        jsonwriter(response)
        return redirect(url_for('gallery'))
    else:
        return redirect(url_for('home'))

@app.route('/delete',methods=['GET', 'POST'])
def delete():
    if request.method=="POST":
        parameters = request.form.to_dict()
        response = BenefitTemplateService.create(parameters)
        jsondelete(response)

        return redirect(url_for('edit'))
    else:
        return 'this is not a post'


if __name__ == '__main__':
    #Guildname()
    app.run(host='0.0.0.0')
