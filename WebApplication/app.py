from flask import Flask
from flask import request
from flask import render_template
import os
import logging

app = Flask(__name__)

# This part is needed for the showTestLabel function. When we open text files in flask, unlike the Jinja HTML, it isn't smart enough to know that it is in the current flask directory. So you can't specify relative paths and expect it to know what you're talking about. When you type: 'static/true_label/...' it's not going to look for the static folder inside the current directory, it is going to look for it like this 'C:\static\true_label'. It looks at absolute paths, and thus won't find anything. Here we are defining the absolute path in such a way that anybody running this code will be able to use it without problem

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) # gets absolute path of the directory this file is in.
TRUE_LABEL_FOLDER = os.path.join(APP_ROOT, 'static/true_label')
app.config['TRUE_LABEL_FOLDER'] = TRUE_LABEL_FOLDER


Audios = ["Audio 1", "Audio 2", "Audio 3", "Audio 4", "Audio 5", "Audio 6", "Audio 7", "Audio 8", "Audio 9", "Audio 10"]
audio_files = ["interaction1.wav", "interaction2.wav", "interaction3.wav", "interaction4.wav", "interaction5.wav", "interaction6.wav", "interaction7.wav", "interaction8.wav", "interaction9.wav", "interaction10.wav"]

@app.route('/')
def index() :
    return render_template("index.html", Audios = Audios, audio_files = audio_files)
    # when you render template remember to import it with 'from flask import render_template'

@app.route('/testlabel<id>', methods=['POST'])
def showTestLabel (id) :
    if request.method == 'POST':
    # when you use request remember to import it
        with open(TRUE_LABEL_FOLDER + '/true_label' + id + '.txt', "r") as f:
            content = f.read()
        return render_template("index.html", Audios = Audios, audio_files = audio_files, id = int(id), which = "true", content = content) # id is a string taken from the url, we have to convert to int in order to compare it to loop.index in the html
        
@app.route('/googleAPI<id>', methods=['POST'])
def showGoogle (id) :
    if request.method == 'POST' :
        return render_template("index.html", Audios = Audios, audio_files = audio_files, id = int(id), which = "google")

@app.route('/amazonAPI<id>', methods=['POST'])
def showAmazon (id) :
    if request.method == 'POST' :
        return render_template("index.html", Audios = Audios, audio_files = audio_files, id = int(id), which = "amazon")

@app.route('/azureAPI<id>', methods=['POST'])
def showAzure (id) :
    if request.method == 'POST' :
        return render_template("index.html", Audios = Audios, audio_files = audio_files, id = int(id), which = "azure")