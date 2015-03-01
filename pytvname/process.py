#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    pytvname.process
    ~~~~~~~~~~~~~~~~

    Tv show name processment.

"""

import re, json

class StringValueError(ValueError):
    """
    The parametes must be a string error.
    """
    def __init__(self, message = 'The parameter must be a string.'):
        ValueError.__init__(self, message)

class Teams(object):
    """
    This class handles team names database
    in json format.
    """

    def __init__(self, filePath = 'resources/teams.json'):
        """
        Sets json filePath and loads it.

        Params
        ======
        filePath <str>: the json database path.

        """
        self.file = '\\'.join(__file__.split('\\')[:-1]) + '\\' + filePath
        self.load()

    def load(self):
        with open(self.file, 'r') as fp:
            self.names = json.load(fp)
        self.names['names'] = set(self.names['names'])

    def save(self):
        self.names['names'] = list(self.names['names'])
        with open(self.file, 'w') as fp:
            json.dump(self.names, fp, sort_keys = True, indent = 4, ensure_ascii = False)

    def add(self, name):
        """
        Adds a name in the list and returns itself.

        Params
        ======
        name <str>: the name to be added.

        """
        self.names['names'].add(name)
        return self

    def find(self, fragment):
        """
        Tries to find one of the names in the database.

        Params
        ======
        fragment <str>: fragment utilized in the search

        """
        if type(fragment) != str:
            raise StringValueError()

        # Removes any url in fragment
        fragment = re.sub('(((https?):((//)|(\\\\))|())+(www)+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', '', fragment)
        # Removes any character different from letters and numbers
        fragment = ' ' + re.sub('[^a-z0-9 ]', ' ', fragment.lower()) + ' '
        
        for team in self.names['names']:
            if ' ' + team.lower() + ' ' in fragment:
                return team

        return ''

    def addInterface(self, name = 'team'):
        """
        Interface for adding new values into database.
        """
        try:
            ipt = str(raw_input('Type the ' + name + ' name: '))
        except NameError:
            ipt = str(input('Type the ' + name + ' name: '))
        self.add(ipt).save()

class Qualities(Teams):
    """
    Do exactly the same as Teams class but
    with a different database.
    """
    def __init__(self):
        Teams.__init__(self, 'resources/qualities.json')

    def addInterface(self):
        Teams.addInterface(self, 'quality')

    def find(self, fragments):
        """
        Accepts either a string as fragment or
        list of strings. The list is processed
        in the entered order.

        Params
        ======
        fragments (<str> or <list<str>>): the fragments utilized in the search

        """

        if type(fragments) == str:
            fragments = [fragments]

        for fragment in fragments:
            fragment = fragment.lower()

            qlt = Teams.find(self, fragment)
            
            if qlt != '':
                return qlt

            # Find more general qualities (e.g. 480p, 720p, 1080p ...)
            qlts = re.findall('[0-9]{3,4}p', fragment)
            if len(qlts) > 0:
                return qlts[0]

        return ''

def normalize(fragment):
    """
    Returns the input string normalized. Essentially,
    this function removes unnecessary (for this app)
    fragments from the entered string.

    Params
    ======
    fragment <str>: the string to be normalized.


    Examples
    ========
    >>> from pytvname.process import normalize
    >>> normalize('scandal (2009)')
    'Scandal'
    >>> normalize('[www.down.org]the.mentalist')
    'The Mentalist'
    >>> normalize('arrow.us.720p')
    'Arrow'

    """

    if type(fragment) != str:
        raise StringValueError()

    fragment = ' ' + fragment + ' '

    # Removes any url in fragment
    fragment = re.sub('(((https?):((//)|(\\\\))|())+(www)+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', '', fragment)
    # Removes quality designation (e.g. 720p, 1080p)
    fragment = re.sub('[0-9]{3,4}p', '', fragment)
    # Removes any character different from letters and numbers
    fragment = re.sub('[^a-zA-Z0-9 ]', ' ', fragment)
    # Tries to remove any year from fragment (e.g. 2009)
    fragment = re.sub('[0-9]{4}', '', fragment)

    # Removes these fwords from fragment
    fwords = ['us','uk','hdtv']
    for fword in fwords:
        fragment = fragment.replace(' ' + fword + ' ', '')

    # Removes double spaces;
    # Removes spaces at the beggining and ending
    # Uppercase on first leters of all words
    return re.sub('[ ]{2,}', '', fragment).strip().title()

def info(name):
    """
    Tries to get information from a name
    running some regex patterns and returns
    this information in dictionary form.

    The information are: show name, season
    and episode numbers, release team name
    and release quality.

    Params
    ======
    name <str>: the name used in the search.

    Examples
    ========
    >>> from pytvname.process import info
    >>>
    >>> info('Banshee.S03e07.HDTV.x264-KILLERS[ettv]')
    {'showName': 'Banshee', 'seasonNum': '03', 'episodeNum': '07', 'teamName': 'KILLERS', 'quality': 'HDTV'}
    >>>
    >>> info('vikings 01x01.web.dl')
    {'showName': 'Vikings', 'seasonNum': '01', 'episodeNum': '01', 'teamName': 'WEB DL', 'quality': ''}
    >>>
    >>> info('The.Big.Bang.Theory.8x16.HDTV.x264-LOL')
    {'showName': 'The Big Bang Theory', 'seasonNum': '08', 'episodeNum': '16', 'teamName': 'LOL', 'quality': 'HDTV'}
    
    """

    if type(name) != str:
        raise StringValueError()
    
    # Search patterns in this order
    patterns = ['(.*)s(\d{1,2})e(\d{1,2})(.*)', '(.*)(\d{2})x(\d{2})(.*)', '(.*)(\d{1,2})x(\d{1,2})(.*)']
    searches = [re.match(pat, name, re.IGNORECASE) for pat in patterns]
    
    # Standard values for showName, seasonNum, episodeNum and teamName
    values = None

    if searches[0]:
        values = searches[0].groups()
    elif searches[1]:
        values = searches[1].groups()
    elif searches[2]:
        values = searches[2].groups()

    teams     = Teams()
    qualities = Qualities()

    if not values:
        return None

    return {
        'showName'  : normalize(values[0]),
        'seasonNum' : str(values[1]).zfill(2),
        'episodeNum': str(values[2]).zfill(2),
        'teamName'  : teams.find(values[3]),
        'quality'   : qualities.find([values[3], values[0]])
    }

def applyfuncs(value, funcs):
    """
    Apply basic str functions on value.

    Param
    =====
    value <str>: the str fragment to perform the functions.
    funcs <list<str>>: list of functions to be applied.

    Examples
    ========
    >>> from pytvname.process import applyfuncs
    >>> applyfuncs('house of cards', ['upper'])
    'HOUSE OF CARDS'
    >>> applyfuncs('The BIG bang ThEoRy', ['title'])
    'The Big Bang Theory'

    """

    # Verify the params types
    if type(value) != str:
        raise StringValueError()

    for func in funcs:
        if type(func) != str: raise StringValueError()

    # Function dict
    f = {
        'lower': str.lower,
        'upper': str.upper,
        'title': str.title,
        'zfone': lambda x: str(int(x)).zfill(1),
        'zftwo': lambda x: str(int(x)).zfill(2),
    }

    for func in funcs:
        if func in f:
            value = f[func](value)

    return value

def prc(name, format = '{showName} S{seasonNum}E{episodeNum} {teamName}'):
    """
    Process a given name into a given format.
    
    This format is composed with keywords in the
    form: {keyword}. Also, each keyword allows the
    application of some string functions in the form:
    {keyword.func1.func2}.

    Params
    ======
    name <str>: name to be processed.
    format <str>: the return format of processment.

    Examples
    ========
    >>> from pytvname.process import prc
    >>> prc('Banshee.S03E07.HDTV.x264-KILLERS[ettv]')
    'Banshee S03E07 KILLERS'
    >>>
    >>> original = 'vikings.s01e01.rites.of.passage.720p.web.dl.sujaidr'
    >>> format = '{showName} S{seasonNum}E{episodeNum} {quality} {teamName}'
    >>> prc(original, format)
    'Vikings S01E01 720p WEB DL'
    >>>
    >>> original = 'Banshee.S03E08.HDTV.x264-KILLERS[ettv]'
    >>> format = '{showName.lower}.{seasonNum.zfone}{episodeNum}.{teamName.lower}'
    >>> prc(original, format)
    'banshee.308.killers'

    """

    # Possible format keywords:
    # - showName      (e.g. The Mentalist)
    # - seasonNumber  (e.g. 03)
    # - episodeNumber (e.g. 10)
    # - teamName      (e.g. LOL)
    # - quality       (e.g. HDTV)

    keywords = info(name)

    if not keywords:
        return None

    prcname  = format

    # find keywords to replace in prcname
    for keyfunc in re.findall('\{[a-zA-Z.]{1,}\}', format):
        # removes the brackets from keyword
        keyfunc = keyfunc[1:-1]

        # the actual keyword is the first word before the dot
        key = keyfunc.split('.')[0]

        # if this information is available, replace the keyword
        if key in keywords:
            value   = str(keywords[key])

            # apply functions on value
            value   = applyfuncs(value, keyfunc.split('.')[1:])

            prcname = prcname.replace('{' + keyfunc + '}', value)

    return prcname