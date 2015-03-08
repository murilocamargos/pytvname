#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Module not tested

import os, shutil

class Path(object):
    """
    This class offers a path utility.
    This is something like the pathlib
    package from python 3.
    """

    def __init__(self, path):
        self.normpath = lambda path: os.path.normpath(path).replace('\\', '/').strip('/')
        self.path = self.normpath(path)
        
        if self.path[-1] == ':':
            self.path += '/'

    def walk(self):
        """
        Walks trough a directory.
        """
        if not self.is_dir():
            return []
        return os.walk(self.path)

    def is_dir(self):
        """
        Verifies if the path path exists as
        a directory.
        """
        return os.path.isdir(self.path)

    def suffix(self):
        """
        Gets the extension of a file path.
        """
        return os.path.splitext(self.path)[1]

    def parent(self):
        """
        Returns the first parent of a path.
        """
        return Path('/'.join(self.path.split('/')[:-1]))

    def parents(self):
        """
        Returns all of the parents of a path.
        """
        parents = []

        prt = self.parent()

        while True:
            if parents != [] and parents[-1] == prt: break
            
            parents += [prt]
            prt = prt.parent()

        return parents

    def create_path(self):
        """
        Creates the given path with its parents.
        """
        created = []
        paths = [self] if self.is_dir() else []
        paths += self.parents()
        for path in paths[::-1]:
            if not path.is_dir() and path.mkdir():
                created += [path]
        return created

    def is_empty(self):
        """
        Checks if a dir is empty.
        """
        if not self.is_dir():
            return False
        return os.listdir(self.path) == []

    def mkdir(self):
        """
        Creates the directory if possible.
        """
        if not self.is_dir():
            try:
                self.parent().chmod(0777)
                os.mkdir(self.path)
            except:
                return False
        return True

    def exists(self):
        """
        Checks if the path exists.
        """
        return os.path.exists(self.path)

    def chmod(self, perm):
        """
        Sets permission on path.
        """
        if not self.exists():
            return False
        try:
            os.chmod(self.path, perm)
            return True
        except:
            return False

    def join(self, fragment):
        """
        Join a fragment path to the global path.
        And returns a new Path.
        """
        return Path(self.path + '/' + self.normpath(fragment))

    def name(self, suffix = False):
        """
        Returns the name of the file,
        with or without the suffix.
        """
        name = self.path.split('/')[-1]
        
        if suffix:
            return name

        return name.replace(self.suffix(), '')

    def strp(self, fragment):
        """
        Strip fragment from path.
        """
        fragment = str(fragment)
        size = len(str(fragment))
        name = str(self.path)
        
        if name[-size:] == fragment:
            name = name[:-size]
        if name[:size] == fragment:
            name = name[size:]
            
        return name

    def rename(self, newName):
        """
        Renames file or directory with
        given name.
        """
        self.chmod(0777)
        shutil.move(self.path, str(newName))

    def rmdir(self):
        """
        Deletes an empty directory.
        """
        if not self.is_empty():
            raise Exception('This functions only works with empty directories.')

        self.chmod(0777)
        os.rmdir(self.path)

    def unlink(self):
        """
        Deletes the path if it represents
        a file.
        """
        if self.is_dir():
            raise Exception('You must use rmdir function to erase a directory.')

        self.chmod(0777)
        os.remove(self.path)

    def __repr__(self):
        return self.path

    def __str__(self):
        return str(self.path)

    def __eq__(self, obj2):
        return self.path == obj2.path

    def __ne__(self, obj2):
        return self.path != obj2.path

    def __hash__(self):
        return hash(self.path)


class Table:
    """
    This class is an utilitary to show nice
    tables is the terminal.
    """
    def __init__(self, **args):
        if 'width' not in args:
            raise ValueError('You must provide the width <int> for this table.')
        if 'title' not in args:
            raise ValueError('You must provide the title <str> for this table.')
        if 'rows' not in args:
            raise ValueError('You must provide the rows <list<str>> for this table.')

        self.width = args['width']
        self.title = args['title']
        self.rows  = args['rows']

    def horizontal_line(self):
        return '+' + '-' * (self.width - 2) + '+'

    def center_text(self, text, delim = '|'):
        space = self.width - len(delim) * 2 - len(text)
        left  = space // 2
        right = space - left
        return delim + ' ' * left + text + ' ' * right + delim

    def frm_row(self, text, delim = '|'):
        space = self.width - (len(delim) + 1) * 2  - len(text)
        if space < 0:
            text = text[:space-3] + '...'
        text += ' '
        return delim + ' ' + text + ' ' * space + delim

    def get(self):
        tbl = self.horizontal_line() + '\n'
        tbl += self.center_text(self.title) + '\n'
        tbl += self.horizontal_line() + '\n'

        for item in self.rows:
            tbl += self.frm_row(item) + '\n'

        tbl += self.horizontal_line() + '\n'

        return tbl

    def __str__(self):
        return self.get()