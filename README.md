# MaSC_compendium_helper
Helper scripts for reading, understanding, and preprocessing the NYUAD music compendium



## Tools



* `metadata.py`

​	**Description** : get a pandas DataFrame saved in PyTables structure in an HDF5 (.h5) file from selected columns of a comma-separated .csv file with table of metadata <br>

​	**Instructions** : run with python3 using the arguments `--metadata_path` with the path of the .csv file with the metadata, `--tags_path` with the path of the .txt file containing the desired metatarsi separated by a newline, and `--output_dir` for the desired directory of the .h5 file output. If no tags file is specified, all metatags are loaded and saved. If no output directory is specified, output is defaulted to current working directory. Example: <br> 

   ```python
   python3 metadata.py --metadata_path=/Users/MaSC/Arab_Mashriq/metadata.csv --tags_path=/Users/MaSC/Arab_Mashriq/tags.txt --ouput_path=/Users/MaSC/Arab_Mashriq
   ```

