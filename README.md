# Directory Cleaner



Simple python script to Clean up your download Directory. Categorises Each file in a directory and is capable of working recursively in a directory

##### Capablities

- Parsing external json files to categorise each file type
- Categorise files based on their size (Minimum size currently)
- Recursively walk through subdirectories(Should be used carefully because it might   alter directory structure completely)
- Work with any directory through command line

# Platforms

- Linux
- Mac(Not tested)
- Windows(Not tested)
# Options 
- --dir [DIR]           Directory to run against

- -r       Recursively Scan sub directories

- -d , --default 
                      Work with default folder (~/Downloads folder)

-   -v , --verbose 
                        Show files scanned

#  Config Files

#####  file_types.json Sample format
#####  _
```json
{
    "<Folder Name>": "<File Type as comma seperated list>"
    "Example" : ".type1,type2,tyep3"
}
```

#####  file_types.json Sample format
#####  _
```json
{
    "<Folder Name>": "<File Type as comma seperated list>"
    "Example" : ".type1,type2,tyep3"
}
```


#####  file_sizes.json Sample format
#####  _
```json
{
    "<Folder Name>": {
      "file_cats": ["<Existing Folder Name in file_types.json>",...],
      "min_size": type:int "<Minimum File Size (Matches all files >= min_size)>"
    }
}
```

