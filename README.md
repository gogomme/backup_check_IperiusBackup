# backup check IperiusBackup

## The objective

The purpose of this script is to check the backup jobs status of the "Iperius Backup" freeware for Windows OS.

<p align="center">
  <img src="https://images.g2crowd.com/uploads/product/image/social_landscape/social_landscape_47dade7fb5f5758b8b79435ef85982f8/iperius-backup.png" alt="IperiusBackup logo" width="300"/>
</p>

## The context

This script has been designed for use in the "Tactical RMM" monitoring solution, which allows scripts to be launched from agents installed on machines. Python is also installed in the agent folder.

The monitoring solution determines whether the task is correct or in error according to the return code sent. 

## Operating principle

Iperius backup generates an html log called "LogFile.htm" which is always the last task executed.

This file is always stored at location "C:\ProgramData\IperiusBackup\Logs\Job001\LogFile.htm" and line 23 of the HTML gives the job status. (example for 1 job)

In Python, the "bs4" module with the "beautifulsoup4" class can be used to analyze and extract the tag content in specific lines (here 23).

In a based Pyhton installation, the module need to be downloaded with pip before.

```pyton
# This module is needed to execute the pip command
import subprocess

# Try import the module, if import error execute the pip installation
try:
    import bs4
except ImportError:
    subprocess.check_call([
        "python", "-m", "pip", "install", "beautifulsoup4"
        ])

# Retry import the module
import bs4

# Import the class
from bs4 import BeautifulSoup
```
Once we've obtained the content of the desired html tag, we can simply check its state with if, else. 

### Result

**Note :** The script verify french character string, modify it for other languages.

There are 4 possible scenarios:

- result is none, the log file is unreachable or empty. The return code is 1 for "Error".
- result is "Sauvegarde terminée avec des avertissements", the log file exist but Iperius notice no changes in his job with the previous backup, The return code is 1 for "Error".
- result is "Sauvegarde terminée avec succès", the log file exist and the job backup is succeful. The return code is 0 for "Successful".
- result is other, the log file exist but the job backup has error(s). The return code is 1 for "Error"
