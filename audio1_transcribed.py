''' 
This file will be reused to extract the
necesssary information from 9 other audio files.
Only two things need to change for each audio file:
1) The xml file path (file_name)
2) The speaker list (speakers)
'''
from zipfile import ZipFile 
from xml.etree import ElementTree
from collections import OrderedDict 
  
# Parameters for both functions
folder_name = "E:/dm0469/Documents/TEXTBOOKS/MSAI/Fall 2020/CSCE 5214/Persona"
  
wav_file = 'Bed010' # Choose the wav file

speakers = ['A', 'B', 'C', 'D', 'E', 'F', 'G'] # Check how many speakers in ICSI dataset

def extract_zip(folder_location, wav_name, speaker_list):
    
    zip_file = folder_location + '/ICSI_core_NXT.zip'
    
    # Opening the zip file in READ mode 
    with ZipFile(zip_file, 'r') as zip: 
        # Extracting all the files 
        print('Extracting all the files now...') 
        
        # Zip.extractall()
        for speaker in speaker_list:
            file = 'ICSI/Words/{}.{}.words.xml'.format(wav_name, speaker)
            zip.extract(path=folder_location, member=file)
            
        print('Done!\n')     


def speaker_diarization(folder_location, wav_name, speaker_list):
    label = 0
    dict_of_words = {}
    
    # This will loop through each speaker file per audio    
    for speaker in speaker_list:    
        # Get our xml file
        xml_file = folder_location + '/ICSI/Words/{}.{}.words.xml'.format(wav_name, speaker)    
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
            if (2100 <= end_time <= 2146) and punc == 'W': # Choose time range (in seconds)
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