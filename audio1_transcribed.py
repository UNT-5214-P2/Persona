''' 
This file will be reused to extract the
necesssary information from 9 other audio files.
Only two things need to change for each audio file:
1) The xml file path (file_name)
2) The speaker list (speakers)
'''
# Importing required modules
from zipfile import ZipFile 
from xml.etree import ElementTree
from collections import OrderedDict 
  
# Specifying the zip file name 
file_name = "D:\Documents\ICSI Dataset\ICSI_core_NXT.zip"
  
# Opening the zip file in READ mode 
speakers = ['A', 'B', 'C', 'D', 'E', 'F']

with ZipFile(file_name, 'r') as zip: 
    # Extracting all the files 
    print('Extracting all the files now...') 
    
    # Zip.extractall()
    for speaker in speakers:
        file = 'ICSI/Words/Bdb001.{}.words.xml'.format(speaker)
        zip.extract(path='D:\Documents\ICSI Dataset', member=file)
        
    print('Done!\n')     

label = 0
dict_of_words = {}

# This will loop through each speaker file per audio    
for speaker in speakers:    
    # Get our xml file
    xml_file = 'D:\Documents\ICSI Dataset\ICSI\Words\Bdb001.{}.words.xml'.format(speaker)    
    dom = ElementTree.parse(xml_file)    
    
    # Filter file to word attribute
    words = dom.findall('w')
    
    # Extract words and label
    for w in words:
        # Filter punctuation
        punc = w.get('c')        
        
        # End time attribute
        end_time = w.get('endtime')
        
        # Start time attribute
        start_time = w.get('starttime')

        if start_time == '' and end_time == '':
            continue
        
        elif start_time == '':
            end_time = float(end_time)
            start_time = end_time
        
        elif end_time =='':
            end_time = float(start_time)
            start_time = end_time
            
        else:
            end_time = float(end_time)
            start_time = float(start_time)
        
        # Create map of maps
        if end_time <= 46 and punc == 'W':
            time = start_time
            dict_of_words[time] = {w.text: label}
            
    # Update label for next speaker
    label += 1
       
# Reorder Dictionary
dict_of_words_ordered = OrderedDict(sorted(dict_of_words.items())) 

# Create lists for words and speakers
words_list = []
speaker_list = []

for time in dict_of_words_ordered:
    for word, speaker in dict_of_words_ordered[time].items():
        words_list.append(word)
        speaker_list.append(speaker)

# Normalize speaker list
speaker_list_dict = {}

label_normalizer = 0

for speaker in speaker_list:
    if speaker in speaker_list_dict:
        continue
    else:
        speaker_list_dict[speaker] = label_normalizer
        label_normalizer += 1
        
print(f"Normalized Labels: {speaker_list_dict}\n")

# Normalize labels
speaker_list_normalized = [speaker_list_dict[tag] for tag in speaker_list]
print(speaker_list_normalized, '\n')

# initialize an empty string  for text output
string = " " 

# Output text file string   
print(string.join(words_list))