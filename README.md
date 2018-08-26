# Directory Cleaner



Simple python script to Clean up your download Directory. Categorises Each file in a directory and is capable of working recursively in a directory

##### Capablities

- Parsing external json files to categorise each file type
- Categorise files based on their size (Minimum size currently)
- Recursively walk through subdirectories(Should be used carefully because it might   alter directory structure completely)
- Work with any directory through command line

# Platforms

- Linux
- Windows
- Mac(Not tested)
# Options 
- **--dir [DIR]**           Directory to run against
- **--config [CONFIG]**     JSON file in predefined format to sort files by its
                        extension
- **-r , --recursive**
                        Recursively Scan sub directories
- **-c , --clean**
                        Clean empty directories created after categorisation
- **-a , --all**
                        Scan all files (. files too)
- **-d , --default**
                        Work with default folder (~/Downloads folder)
- **-v , --verbose** 
                        Show verbose output
                        
- **-h, --help**        show  help and exit

#  Config Files


#####  Sample format for configuration file --config
```json
{
    "Categories":{
        "<Folder Name>": "<File Type as comma seperated list>",
        "Example" : ".type1,type2,tyep3"
    },
    "Sizes":{
        "<Folder Name>": {
            "file_cats": ["<Existing Folder Name in file_types.json>","..."],
            "min_size": " type:int in MegaBytes:  <Minimum File Size (Matches all files >= min_size)>"
        }
    },
    "FallbackDir":"Directory to put unknown files",
    "IgnoreFiles":[
      "<Regular expressions to find file>"
    ]
}
```

