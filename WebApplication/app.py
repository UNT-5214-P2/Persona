from flask import Flask
from flask import request
from flask import render_template
from google.cloud import speech_v1p1beta1 as speech
from sklearn.metrics.cluster import adjusted_rand_score
import io
import os
import logging

app = Flask(__name__)
app.config['API_KEYS'] = './API_KEYS/'
app.config['AUDIO_FILES'] = './static/wav/'
app.config['TRUE_LABEL'] = './static/true_label/'

# This part is needed for the showTestLabel function. When we open text files in flask, unlike the Jinja HTML, it isn't smart enough to know that it is in the current flask directory. So you can't specify relative paths and expect it to know what you're talking about. When you type: 'static/true_label/...' it's not going to look for the static folder inside the current directory, it is going to look for it like this 'C:\static\true_label'. It looks at absolute paths, and thus won't find anything. Here we are defining the absolute path in such a way that anybody running this code will be able to use it without problem

APP_ROOT = os.path.dirname(os.path.abspath(__file__)) # gets absolute path of the directory this file is in.
TRUE_LABEL_FOLDER = os.path.join(APP_ROOT, 'static/true_label')
app.config['TRUE_LABEL_FOLDER'] = TRUE_LABEL_FOLDER


Audios = ["Audio 1", "Audio 2", "Audio 3", "Audio 4", "Audio 5", "Audio 6", "Audio 7", "Audio 8", "Audio 9"]
audio_files = ["interaction1.wav", "interaction2.wav", "interaction3.wav", "interaction4.wav", "interaction5.wav", "interaction6.wav", "interaction7.wav", "interaction8.wav", "interaction9.wav"]

@app.route('/')
def index() :
    return render_template("index.html", Audios = Audios, audio_files = audio_files)
    # when you render template remember to import it with 'from flask import render_template'

@app.route('/get_rand', methods=['GET'])
def get_rand() :
    return render_template("what_is_rand.html")

@app.route('/testlabel<id>', methods=['POST'])
def showTestLabel (id) :
    if request.method == 'POST':
        word_file_name = "words_" + id + ".txt"
        words = os.path.join(app.config['TRUE_LABEL'], word_file_name)
        with open(words, "r") as f:
            content_words = f.read()

        speaker_ids_file_name = "speaker_id_" + id + ".txt"
        speakerIds = os.path.join(app.config['TRUE_LABEL'], speaker_ids_file_name)
        with open (speakerIds, "r") as f:
            content_speakerIds = f.read()

        return render_template("index.html", Audios = Audios, audio_files = audio_files, id = int(id), which = "true", words = content_words, speakerIds = content_speakerIds) # id is a string taken from the url, we have to convert to int in order to compare it to loop.index in the html
        
@app.route('/googleAPI<id>', methods=['POST'])
def showGoogle (id) :
    if request.method == 'POST' :
        words, speakerIds, randScore = google_api(id)
        return render_template("index.html", Audios = Audios, audio_files = audio_files, id = int(id), which = "google")

@app.route('/amazonAPI<id>', methods=['POST'])
def showAmazon (id) :
    if request.method == 'POST' :
        words, speakerIds, randScore = amazon_api(id) 
        # words, speakerIds, randScore - add this to render_template down below
        return render_template("index.html", Audios = Audios, audio_files = audio_files, id = int(id))

@app.route('/azureAPI<id>', methods=['POST'])
def showAzure (id) :
    if request.method == 'POST' :
        return render_template("index.html", Audios = Audios, audio_files = audio_files, id = int(id), which = "azure")


def google_api(id):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(app.config['API_KEYS'],'Google_Api_Key.json')
    
    audio_file_name = r"interaction" + id + ".wav"
    audio_file_path = os.path.join(app.config['AUDIO_FILES'], audio_file_name)
    
    true_label_file_name = r'speaker_id_' + id + '.txt'
    true_label_path = os.path.join(app.config['TRUE_LABEL'], true_label_file_name) 
    
        # Instantiates a client
    client = speech.SpeechClient()

    # Loads the audio into memory
    with io.open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
    
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_speaker_diarization=True,
        diarization_speaker_count=3
    )
    
    # print("Waiting for operation to complete...\n")
    response = client.recognize(request={"config": config, "audio": audio})
    
    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    result = response.results[-1]
    words_info = result.alternatives[0].words
    
    # Filling list of transcribed words
    list_of_words = []
    
    for word_info in words_info:
        list_of_words.append(word_info.word)
    
    # initialize an empty string  for text output
    string = " " 
    text = string.join(list_of_words)
    
    # Creating list of labels
    speaker_tags = []
        
    for word_info in words_info:
        speaker_tags.append(word_info.speaker_tag)   
    
    # Create new-labels dictionary for speaker tags
    speaker_tags_dict = {}
    counter = 0
    
    for tag in speaker_tags:
        if tag in speaker_tags_dict:
            continue
        else:
            speaker_tags_dict[tag] = counter
            counter += 1

    # Normalize speaker tags
    speaker_tags_normalized = [speaker_tags_dict[tag] for tag in speaker_tags]
    
    # True Labels
    speaker_id_file = open(true_label_path, 'r')
    true_label_id = speaker_id_file.read()
    true_label_speaker_id = []
    
    for c in true_label_id.split(','):
        n = int(c)
        true_label_speaker_id.append(n)
    
    # Setting length of label lists equal
    if len(speaker_tags_normalized) < len(true_label_speaker_id):
        length = len(speaker_tags_normalized)
        true_label_speaker_id = true_label_speaker_id[:length]
    else:
        length = len(true_label_speaker_id)
        speaker_tags_normalized = speaker_tags_normalized[:length]
    
    return text, speaker_tags_normalized, adjusted_rand_score(speaker_tags_normalized, true_label_speaker_id)

    


#def amazon_api(id):