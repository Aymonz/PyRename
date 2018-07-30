import os
import sys

walk_dir = 'vayu'
oldtxt = 'golf'
newtxt = 'skoda'

cfg_extensions = \
    [
        '.c', '.cpp', '.h', '.hpp', '.txt', '.mk',
        '.cmakelists', '.cmake', '.cmd', '.bat',
        '.ini', '.xml', '.py', '.project', '.cproject'
    ]




def TextReplace(oldsubstr: str, newsubstr: str, superstr: str, case_opts='PRESERVE') -> str:

    if len(oldsubstr) != 0:
        idx = 0
        while idx < len(superstr):
            index_l = superstr.casefold().find(oldsubstr.casefold(), idx)

            if index_l == -1:
                return superstr

            if superstr[index_l:(index_l+len(oldsubstr))].isupper() or case_opts == 'UPPER':
                superstr = superstr[:index_l] + newsubstr.upper() + superstr[index_l + len(oldsubstr):]
            elif superstr[index_l:(index_l+len(oldsubstr))].islower() or case_opts == 'LOWER':
                superstr = superstr[:index_l] + newsubstr.lower() + superstr[index_l + len(oldsubstr):]
            else:
                if superstr[index_l].isupper():
                    superstr = superstr[:index_l] + newsubstr[:1].upper() + newsubstr[1:] + superstr[index_l + len(oldsubstr):]
                else:
                    superstr = superstr[:index_l] + newsubstr[:1].lower() + newsubstr[1:] + superstr[index_l + len(oldsubstr):]

            idx = index_l + len(newsubstr)
    return superstr





for root, subdirs, files in os.walk(walk_dir, False):
    print('--\n' + root)

    for subdir in subdirs:
        print('  - ' + subdir)
        if oldtxt.casefold() in subdir.casefold():
            os.rename(os.path.join(root, subdir), os.path.join(root, TextReplace(oldtxt,newtxt,subdir)))

    for file in files:
        print('  - ' + file)

        if os.path.splitext(file.lower())[1] in cfg_extensions:
            with open(os.path.abspath(os.path.join(root, file)), 'r') as f:
                try:
                    oldcontent = f.read()
                except:
                    print('failed file read at' + os.path.join(root, file))
                newcontent = TextReplace(oldtxt,newtxt,oldcontent)

            if (newcontent != oldcontent):
                with open(os.path.abspath(os.path.join(root, file)), 'w') as f:
                    f.write(newcontent)

        if oldtxt.casefold() in file.casefold():
            os.rename(os.path.join(root, file), os.path.join(root, TextReplace(oldtxt,newtxt,file)))