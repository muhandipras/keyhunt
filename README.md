# KeyHunt - Keyword-based File Scanner

Description
------------
KeyHunt is a Python-based tool for scanning files in a directory to identify specific keywords or patterns. It is useful for detecting sensitive information or specific code patterns in source code repositories.

Features
------------
* Recursive directory scanning.
* Keyword-based search.
* Support for multiple file extensions.
* Highlight suspicious patterns like base64_decode.
* Generate formatted output paths starting from the base directory.
* File removal support for suspicious files.

Requirements
------------
* Python 3.7 or higher.
* `tqdm` : For progress bar.

Installing Dependencies
------------
Install the required dependencies using pip:

`pip install tqdm`

Usage
------------
```
usage: python keyhunt.py <directory> -w <wordlist> -ext <extensions> [-rm <file_list>]

Scan files for specified keywords.

positional arguments:
  directory             Directory to scan

options:
  -h, --help            show this help message and exit
  -w, --wordlist WORDLIST
                        Path to the keyword list file
  -ext, --extensions EXTENSIONS
                        Comma-separated list of file extensions to scan
  -rm, --remove REMOVE  Delete files listed in the specified file (e.g., path_file.txt)
  ```

Examples
-------------
* Simple Scan Example:

`python keyhunt.py /Desktop/web -w keywords.txt -ext php,html`
```
Starting scan...
Scanning Files: 100%|██████████████████████████████████████| 14880/14880 [00:31<00:00, 467.09file/s]

Scan complete. List of files with keywords saved to path_file.txt
Detailed scan results saved to scan_results.txt
```

* Remove File Example:

`python keyhunt.py -rm path_file.txt`
