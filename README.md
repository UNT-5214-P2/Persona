# Persona - Speaker Recognition
Overview:

Our Website has below list of 9 audio files sourced from International Computer Science Institute(ICSI) webiste. Labels from this ICSI dataset are consdiered as True Labels.
Clicking on 'True Label (ICSI Data)' button below - shows the list of words, Speaker Diarization Ids parsed from the ICSI XML metadata.
Clicking on 'Google Speech API' button below - Takes the corresponding audio clip, invokes Google Speech API: From the response; displays (a) Predicted words (b) Predicted Speaker Diarization Ids and (c) Rand score between true label Speaker Ids & Predicted Speaker Ids.
Clicking on 'Amazon Transcribe API' button below - Takes the corresponding audio clip, invokes Amazon Transcribe API: From the response; displays (a) Predicted words (b) Predicted Speaker Diarization Ids and (c) Rand score between true label Speaker Ids & Predicted Speaker Ids.
What is Rand Score?


Technologies Used:

Website - Flask
● Collaboration - Github
● API Scripts - Python
○ Python packages and libraries (remember to ‘pip install’ these libraries in your virtual
environment! The website will not run and will throw an error otherwise!)
■ Sklearn (pip install sklearn)
■ Google (pip install google)
■ Google-cloud (pip install google-cloud)
■ aws cli (pip install aws cli)
● Once you install these packages, deactivate and then reactivate your virtual
environment before running
