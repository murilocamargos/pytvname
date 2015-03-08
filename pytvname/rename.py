#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Module not tested

from process import prc, info
from utils import Path, Table

def run(**args):
    """
    Runs the renaming tool for tv shows
    files and its subtitles.

    Required params
    ===============
    # path <str>: the path to analize.

    Optional params
    ===============
    # validExts <list<str>>: list of valid extensions.
      default: ['mp4', 'avi', 'mkv', 'str', 'wmv']
    # invalidExts <list<str>>: list of invalid exts, files
      with these extensions will be deleted!
      default: ['txt', 'nfo']

    """

    required = ['path']

    for req in required:
        if req not in args:
            raise ValueError('You must provide the required parameters.')

    path        = Path(args['path'])
    debug       = False if 'debug' not in args else args['debug']
    validExts   = ['mp4', 'avi', 'mkv', 'srt', 'wmv'] if 'validExts' not in args else args['validExts']
    invalidExts = ['txt', 'nfo'] if 'invalidExts' not in args else args['invalidExts']
    format      = '{showName} S{seasonNum}E{episodeNum} {teamName}' if 'format' not in args else args['format']
    ignored     = [] if 'ignored' not in args else [Path(a) for a in args['ignored']]

    def is_ignored(path):
        if type(path) != Path:
            path = Path(path)
        for prt in path.parents():
            if prt in ignored:
                return True
        return path in ignored

    # validate types of params
    #isdir(path)
    #islistof(validExts)
    #islistof(invalidExts)
    #islistog(ignored)

    renamed, rmfiles, rmdirs, created, dirs = [], [], [], [], []

    for (dir, _, files) in path.walk():
        dir = Path(dir)

        if not is_ignored(dir):
            dirs += [dir]

        for file in files:
            filePath = dir.join(file)
            
            if not is_ignored(filePath):
                showInfo = info(filePath.name(True))
                if not showInfo:
                    showInfo = info(filePath.parent().name(True))

                newName = prc(showInfo, format=format)
                extName = filePath.suffix()

                if newName and extName[1:] in validExts and extName[1:] not in invalidExts and 'sample' not in str(filePath).lower():
                    newPath = path.join(showInfo['showName']).join(newName + extName)
                    
                    if newPath != filePath:
                        created += newPath.create_path()
                        filePath.rename(newPath)
                        renamed += [filePath.strp(path), newPath.strp(path), '']

                elif extName[1:] in invalidExts or 'sample' in str(filePath).lower():
                    filePath.unlink()
                    rmfiles += [filePath.strp(path)]

        if dir.is_empty() and not is_ignored(dir):
            dir.rmdir()
            rmdirs += [dir.strp(path)]

    if debug:
        if rmfiles != []:
            tbl = Table(title = 'Removed Files', width = 70, rows = rmfiles)
            print(tbl)

        if renamed != []:
            tbl = Table(title = 'Renamed Files', width = 70, rows = renamed)
            print(tbl)

        if created != []:
            created = [c.strp(path) for c in created]
            tbl = Table(title = 'Created Dirs', width = 70, rows = created)
            print(tbl)

        if rmdirs != []:
            tbl = Table(title = 'Removed Dirs', width = 70, rows = rmdirs)
            print(tbl)


run(path='D:\Series', debug=True)#format='{showName.lower.dtspc}.{seasonNum.zfone}{episodeNum}.{teamName.lower.rmspc}')

