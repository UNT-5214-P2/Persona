# Persona - Speaker Diarization
Overview:

* Our Website has list of 9 audio files sourced from the International Computer Science Institute (ICSI) website. Labels from this ICSI dataset are considered as True Labels.
* Clicking on 'True Label (ICSI Data)' button below - shows the list of words and Speaker Diarization Ids parsed from the ICSI XML metadata.
* Clicking on 'Google Speech API' button below - Takes the corresponding audio clip and invokes the Google Speech API: From the response, displays (a) Predicted words (b) Predicted Speaker Diarization Ids and (c) Rand score between true label Speaker Ids & Predicted Speaker Ids.
* Clicking on 'Amazon Transcribe API' button below - Takes the corresponding audio clip and invokes Amazon Transcribe API: From the response, displays (a) Predicted words (b) Predicted Speaker Diarization Ids and (c) Rand score between true label Speaker Ids & Predicted Speaker Ids.
* What is Rand Score? - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.adjusted_rand_score.html


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
