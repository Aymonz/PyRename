import os
import sys
from typing import List, Tuple

################################# CFG #####################################
walk_dir = '../../autosim'

SyllablesMap = [('auto','drive'), ('sim','sim')]

cfg_extensions = []
'''     [
        '.c', '.cpp', '.h', '.hpp', '.txt', '.mk',
        '.cmakelists', '.cmake', '.cmd', '.bat',
        '.ini', '.xml', '.py', '.project', '.cproject'
    ] '''

verbose = False

############################# Helper Funcs ################################

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

def InferNewTxtFromOldTxt(oldstr: str, SyllablesMap: List[Tuple[str,str]]) -> str:
    outstr = oldstr
    for t in SyllablesMap:
        oldsyll = t[0]
        newsyll = t[1]
        outstr = TextReplace(oldsyll, newsyll, outstr)
    return outstr

def RenameIntext(oldsubstr: str, superstr: str, SyllablesMap: List[Tuple[str,str]]) -> str:
    idx = 0
    while idx < len(superstr):
        index_l = superstr.casefold().find(oldsubstr.casefold(), idx)
        
        if index_l == -1:
            return superstr

        newsubstr = InferNewTxtFromOldTxt(superstr[index_l:(index_l+len(oldsubstr))], SyllablesMap)

        superstr = superstr[:index_l] + newsubstr + superstr[index_l + len(oldsubstr):]

        idx = index_l + len(newsubstr)

    return superstr

################################# MAIN ####################################

OldTxt = ''
NewTxt = ''
for t in SyllablesMap:
    OldTxt = OldTxt+t[0]
    NewTxt = NewTxt+t[1]


for root, subdirs, files in os.walk(walk_dir, False):
    if verbose: print('--\n' + root)

    for subdir in subdirs:
        if verbose: print('  - ' + subdir)

        abspath = os.path.abspath(os.path.join(root, subdir))

        if os.path.islink(abspath):
            oldTarget = os.readlink(abspath)
            newTarget = RenameIntext(OldTxt, oldTarget, SyllablesMap)
            if (newTarget != oldTarget):
                os.unlink(abspath)
                os.symlink(newTarget, abspath)
                print('Changed Directory Symlink at: ' + abspath + ' Target ' + oldTarget + ' -> ' + newTarget)

        if OldTxt.casefold() in subdir.casefold():
            os.chmod(abspath, 0o777)
            newName = RenameIntext(OldTxt, subdir, SyllablesMap)
            os.rename(os.path.join(root, subdir), os.path.join(root, newName))
            print('renamed Directory at: ' + abspath + ' Name ' + subdir + ' -> ' + newName)

    for file in files:
        if verbose: print('  - ' + file)

        abspath = os.path.abspath(os.path.join(root, file))

        if os.path.islink(abspath):
            oldTarget = os.readlink(abspath)
            newTarget = RenameIntext(OldTxt, oldTarget, SyllablesMap)
            if (newTarget != oldTarget):
                os.unlink(abspath)
                os.symlink(newTarget, abspath)
                print('Changed File Symlink at: ' + abspath + ' Target ' + oldTarget + ' -> ' + newTarget)
            

        elif (os.path.splitext(file.lower())[1] in cfg_extensions) or (len(cfg_extensions)==0):
            os.chmod(abspath, 0o777)
            oldcontent=''
            newcontent=''
            with open(abspath, 'r') as f:
                try:
                    oldcontent = f.read()
                    newcontent = RenameIntext(OldTxt, oldcontent, SyllablesMap)
                except:
                    if verbose: print('failed file read at ' + os.path.join(root, file))

            if (newcontent != oldcontent):
                with open(abspath, 'w') as f:
                    f.write(newcontent)
                    print('Changed Content of File: ' + abspath)

        if OldTxt.casefold() in file.casefold():
            newName = RenameIntext(OldTxt, file, SyllablesMap)
            os.rename(os.path.join(root, file), os.path.join(root, newName))
            print('renamed File at: ' + abspath + ' Name ' + file + ' -> ' + newName)

print('Normal termination ... Please check results!')