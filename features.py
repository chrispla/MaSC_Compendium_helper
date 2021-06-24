"""
Script to compute audio features for the audio recordings in the Arab Mashriq collection.
The script goes through the audio files and computes their MFCCs, Chromagram, and Tempogram.
Since the metadata file with all recordings, tags, and values is based off of the audio
paths, the features can be easily associated with the metadata. Since there is no NYUAD
Archival Reference for most recordings, a dictionary of 'mfcc', 'chromagram', and
'tempogram' for each recording is stored in a parent dictionary with the file paths
relative to the parent audio directory as keys.
"""

import librosa #feature computation
from pathlib import Path #directory traversal
import pandas as pd #read metadata DataFrame
import argparse #parse command line arguments
import deepdish as dd #save python dictionary to HDF5
import sys #display computation progress
import warnings #to filter warnings
from tables import NaturalNameWarning #to filter naming warning from PyTables

# Argument parser
parser = argparse.ArgumentParser(description="audio and output directories")
parser.add_argument("--audio_dir", default='.')
parser.add_argument("--output_dir", default='.')
args = parser.parse_args()
audio_dir = args.audio_dir
output_dir = args.output_dir
audio_dir_len = len(audio_dir)

# filter redundant naming convention warnings from PyTables since we don't use it
# https://stackoverflow.com/questions/58414068/how-to-get-rid-of-naturalnamewarning
warnings.filterwarnings('ignore', category=NaturalNameWarning)

# Check if audio directory exists
if not Path(audio_dir).is_dir():
    raise FileNotFoundError("Invalid audio directory: %s, exiting...", audio_dir)

# Check if output directory exists
if not Path(output_dir).is_dir():
    raise FileNotFoundError("Invalid output directory: %s, exiting...", output_dir)

# Read all paths of audio in directory
audio_paths = []
def files_of(root):
    for p in Path(root).iterdir():
        if p.is_dir():
            files_of(p)
        elif p.is_file() and ('.wav' in str(p) or '.mp3' in str(p) or '.aif' in str(p)):  
            # only get paths of audio files
            audio_paths.append(str(p))
files_of(audio_dir)
print("Found", len(audio_paths), "audio files.")

# Dictionary for audio features
# key : Path relative to parent audio directory
# value : {'mfcc' : np.array, 'chromagram' : np.array, 'tempogram' : np.array}
features = {}

# Traverse audio paths
for i, path in enumerate(audio_paths):  

    # Create feature dictionary
    d = {}

    # Compute features
    y, sr = librosa.load(path)
    d['mfcc'] = librosa.feature.mfcc(y, sr)
    d['chromagram'] = librosa.feature.chroma_stft(y, sr)
    d['tempogram'] = librosa.feature.mfcc(y, sr)

    # add features to dictionary, with the archive reference as key
    features[path[audio_dir_len:]] = d # only keep path relative to audio dir

    # Progress
    sys.stdout.write("\rComputed features for %i audio files." % (i+1))
    sys.stdout.flush()

# Save to HDF5
features_path = Path(output_dir) / 'features.h5'
dd.io.save(features_path, features)
print("Saved features.")
