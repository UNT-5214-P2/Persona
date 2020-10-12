import io
import os

# Imports the Google Cloud client library
from google.cloud import speech_v1p1beta1 as speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "E:\dm0469/Documents\TEXTBOOKS\MSAI\Fall 2020\CSCE 5214\Persona\persona_key.json"

# Instantiates a client
client = speech.SpeechClient()

# The name of the audio file to transcribe
file_name = 'E:\dm0469\Documents\TEXTBOOKS\MSAI\Fall 2020\CSCE 5214\Persona\\interaction1.wav'

# Loads the audio into memory
with io.open(file_name, "rb") as audio_file:
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
    enable_speaker_diarization=True,
    diarization_speaker_count=3
)

print("Waiting for operation to complete...")
response = client.recognize(request={"config": config, "audio": audio})

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
result = response.results[-1]

words_info = result.alternatives[0].words

'''This is the original print statement
from the Google API'''
# Printing out the output:
for word_info in words_info:
    print(f"word: '{word_info.word}', speaker_tag: {word_info.speaker_tag}")



'''Our own print statment'''
print('\n')

# Printing out the output:

speaker_tags = []
    
for word_info in words_info:
    speaker_tags.append(word_info.speaker_tag)
    

print(speaker_tags, '\n')

# Create new-labels dictionary for speaker tags
speaker_tags_dict = {}

counter = 0

for tag in speaker_tags:
    if tag in speaker_tags_dict:
        continue
    else:
        speaker_tags_dict[tag] = counter
        counter += 1
print(f"Normalized Labels: {speaker_tags_dict}")

# Normalize speaker tags
speaker_tags_normalized = [speaker_tags_dict[tag] for tag in speaker_tags]
print(speaker_tags_normalized)
