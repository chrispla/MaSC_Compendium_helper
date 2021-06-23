import pandas as pd
from pathlib import Path
import argparse

# Argument parser
parser = argparse.ArgumentParser(description="input and output path")
parser.add_argument("--metadata_path", required=True) #path of .csv metadata file
parser.add_argument("--tags_path") #path with .txt file of desired metatags
parser.add_argument("--output_dir", default=".") #directory of output
args = parser.parse_args()

metadata_path = args.metadata_path
tags_path = args.tags_path
output_dir = args.output_dir

# Compose output path and check validity
if Path(output_dir).is_dir():
    output_path = Path(output_dir) / 'metadata.h5'

else:
    raise FileNotFoundError("Invalid output directory: %s, exiting...", output_dir)

# Read .csv
metadata = pd.read_csv(metadata_path, sep=',', dtype=str) 

# if tags file is specified, read them
if tags_path:
    with open(tags_path, 'r') as f:
        tags = f.readlines()
        for i in range(len(tags)):
            tags[i] = tags[i].strip()
    # Only keep desired tags
    metadata = metadata[tags]

# Output to HDF5
metadata.to_hdf(output_path, key='df', format='table')
print("Output completed.")
