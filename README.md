# PyRename
is a Python script to globally rename a specific text in a folder structure preserving case.

The script changes:
  - folder_names
  - file_names
  - file_contents
  
For file content change this happens only to files with specified extensions.
  
currently there are only 3 cases for preserving case while replacing:
  - OLDTEXT -> NEWTEXT (All uppercase old text remains all uppercase for new text)
  - Oldtext -> Newtext (Mixed case old text then new text will only follow the case for first letter rest will be lower case)
  - oldtext -> newtext (All lowercase old text remains all lower for new text)
  
  
# Example Usage:
at the begining of the script set the following variables

walk_dir = 'Myprojects\golf_proj'  # relative path to the script.

oldtxt = 'golf'                    # old text to replace.

newtxt = 'skoda'                   # new text.

cfg_extensions = ['.c', '.cpp', '.h', '.hpp', '.txt', '.mk'] # extensions for files for which content will be changed

Then run script!

