import flask_nemo._data
from flask_nemo.common import getFromDict
from collections import OrderedDict
from slugify import slugify
from operator import itemgetter
import sys


def f_hierarchical_passages_full(reffs, citation):
    """ A function to construct a hierarchical dictionary representing the different citation layers of a text

    :param reffs: passage references with human-readable equivalent
    :type reffs: [(str, str)]
    :param citation: Main Citation
    :type citation: Citation
    :return: nested dictionary representing where keys represent the names of the levels and the final values represent the passage reference
    :rtype: OrderedDict
    """
    d = OrderedDict()
    levels = [x for x in citation]
    for cit, name in reffs:
        ref = cit.split('-')[0]
        name = "%{}|{}%".format(levels[-1].name,name)
        levs = ['%{}|{}%'.format(levels[i].name, v) for i, v in enumerate(ref.split('.'))]
        getFromDict(d, levs[:-1])[name] = cit
    return d

def f_i18n_citation_label(string, lang="eng"):
    """ Take a string of form %citation_type|passage% and format it as label

    :param string: String of formation %citation_type|passage%
    :param lang: Language to translate to
    :return: Human Readable string

    .. note :: To Do : Use i18n tools and provide real i18n
    """
    s = string.strip("%").split("|")
    if len(s) > 1:
        return s[0].capitalize()
    else:
        return string

def f_citation_name(string):
    """ Take a string of form %citation_type|passage% and format it as one of the following:
    book, chapter, passage
    :param string: String of formation %citation_type|passage%
    :return: Human Readable string

    .. note :: To Do : Use i18n tools and provide real i18n
    """
    s = string.strip("%").split("|")
    sName = s[0].lower() if len(s) > 1 else string.lower()
    finalName = sName
    if (sName == 'section' or sName == 'line' or sName == 'none'):
        return 'passage'
    return sName

def f_citation_link(string):
    """ Take a string of form %citation_type|passage% and format for the link
    :param string: String of formation %citation_type|passage%
    :return: Human Readable string

    .. note :: To Do : Use i18n tools and provide real i18n
    """
    s = string.strip("%").split("|")
    if len(s) > 1:
        return s[0].lower() + '-' + s[1]
    else:
        return None

def f_i18n_readable_book_title(string):
    """ Take a string of form %citation_type|passage% and format it as a full title for the header:
    :param string: String of formation %citation_type|passage%
    :return: Human Readable string

    .. note :: To Do : Use i18n tools and provide real i18n
    """
    s = string.strip("%").split("|")
    if len(s) > 1:
        return s[0].capitalize() + " " + s[1]
    else:
        return string

def f_i18n_citation_item(string, lang="eng"):
    """ Take a string of form %citation_type|passage% and format it as item only

    :param string: String of formation %citation_type|passage%
    :param lang: Language to translate to
    :return: Human Readable string

    .. note :: To Do : Use i18n tools and provide real i18n
    """
    s = string.strip("%").split("|")
    if len(s) > 1:
        return s[1].capitalize()
    else:
        return string

def f_citation_passage(string):
    """ Take a string of form %citation_type|passage% and return unformatted passage

    :param string: String of formation %citation_type|passage%
    :return: the passage

    """
    s = string.strip("%").split("|")
    if len(s) > 1:
        return s[1]
    else:
        return string

