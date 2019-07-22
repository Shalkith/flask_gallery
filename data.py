import os
import json

def get_images():
    photos = []
    for x in os.listdir('static/photos'):
        if 'jpeg' in x:
            photos.append(x)
    return photos

def jsonreader():
    file = 'static/json/photos.json'
    with open(file) as json_file:
        return json.load(json_file)

def jsonwriter(jsondata):
    file = 'static/json/photos.json'

    with open(file) as json_file:
        currentdata = json.load(json_file)
    update = 0
    for x in currentdata["photos"]:
        if x['file'] == jsondata['file']:
            x['comment'] = x['comment'].replace(x['comment'],jsondata['comment'])
            x['title'] = x['title'].replace(x['title'],jsondata['title'])
            x['hidden'] = x['hidden'].replace(x['hidden'],jsondata['hidden'])
            update = 1
        else:
            pass
    if update == 0:
        currentdata["photos"].append(jsondata)

    with open(file, 'w') as outfile:
        json.dump(currentdata, outfile)


def jsondelete(jsondata):
    file = 'static/json/photos.json'

    with open(file) as json_file:
        currentdata = json.load(json_file)
    for x in currentdata["photos"]:
        if x['file'] == jsondata['file']:
            del currentdata["photos"][currentdata["photos"].index(x)]
            os.remove('static/photos/'+x['file'])
        else:
            pass
    with open(file, 'w') as outfile:
        json.dump(currentdata, outfile)
