#!/usr/bin/env python3
import os
from pprint import pprint
import speaker_verification_toolkit.tools as svt
import sqlite3


# Get a list of files and speakers from audiolog
audiolog_dir=os.path.expanduser('~/.config/naomi/audiolog')
conn = sqlite3.connect("{}/audiolog.db".format(audiolog_dir))
c = conn.cursor()
c.execute(
    " ".join([
        "select",
        "   filename,speaker",
        "from audiolog",
        "where reviewed>''",
        "   and verified_transcription>''",
        "   and speaker>''"
    ])
)
files = c.fetchall()
conn.close()
# separate the files into train and test
train=files[:-10]+files[-9::2]
test=files[-10::2]
print("Train")
pprint(train)
print("Test")
pprint(test)
# Load the train data into an array
train_data=[]
for (filename, speaker) in train:
    print("Loading sample {} of {}".format(len(train_data), len(train)))
    train_data.append(svt.extract_mfcc_from_wav_file(os.path.join(audiolog_dir, filename)))
# Loop through the test data and tell me which voice it matches
for (filename, speaker) in test:
    print("Testing {}, {}".format(filename,speaker))
    match = svt.find_nearest_voice_data(train_data, svt.extract_mfcc_from_wav_file(os.path.join(audiolog_dir,filename)))
    print("{} ({}) matches {} ({})".format(filename, speaker, train[match][0], train[match][1]))
