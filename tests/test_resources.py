import unittest
from flask_nemo import Nemo
from flask import Markup, Flask
from MyCapytain.resolvers.cts.local import CtsCapitainsLocalResolver
from MyCapytain.resolvers.cts.api import HttpCtsResolver
from MyCapytain.retrievers.cts5 import HttpCtsRetriever
from MyCapytain.resources.collections.cts import XmlCtsTextInventoryMetadata
from MyCapytain.resources.prototypes.cts.inventory import CtsTextInventoryCollection
from MyCapytain.resolvers.utils import CollectionDispatcher
from alpheios_nemo_ui import scheme_grouper, level_grouper
import logging


def create_test_app(debug=False, config=None):
    app = Flask(__name__)
    app.debug = debug

    if config:
        app.config.update(**config)
    return app


class RequestPatch(object):
    """ Request patch object to deal with patching reply in flask.ext.nemo
    """
    def __init__(self, f):
        self.__text = f.read()

    @property
    def text(self):
        return self.__text


class RequestPatchChained(object):
    """ Request patch object to deal with patching reply in flask.ext.nemo
    """
    def __init__(self, requests):
        self.resource = [other.text for other in requests]

    @property
    def text(self):
        return self.resource.pop(0)


class NemoResource(unittest.TestCase):
    """ Test Suite for Nemo
    """
    endpoint = HttpCtsResolver(HttpCtsRetriever("http://website.com/cts/api"))
    body_xsl = "tests/test_data/xsl_test.xml"

    def setUp(self):
        with open("tests/test_data/getcapabilities.xml", "r") as f:
            self.getCapabilities = RequestPatch(f)

        with open("tests/test_data/getvalidreff.xml", "r") as f:
            self.getValidReff_single = RequestPatch(f)
            self.getValidReff = RequestPatchChained([self.getCapabilities, self.getValidReff_single])

        with open("tests/test_data/getpassage.xml", "r") as f:
            self.getPassage = RequestPatch(f)
            self.getPassage_Capabilities = RequestPatchChained([self.getCapabilities, self.getPassage])

        with open("tests/test_data/getpassageplus.xml", "r") as f:
            self.getPassagePlus = RequestPatch(f)

        with open("tests/test_data/getprevnext.xml", "r") as f:
            self.getPrevNext = RequestPatch(f)
            self.getPassage_Route = RequestPatchChained([self.getCapabilities, self.getPassage, self.getPrevNext])

        self.nemo = Nemo(
            resolver=NemoResource.endpoint,
            app=Flask(__name__)
        )

class TestChunker(unittest.TestCase):

    """ Test different chunker params

    """

    def test_special(self):
        """ Tests rules for specific texts
        """
        text = NautilusDummy.getTextualNode('urn:cts:latinLit:stoa0040.stoa062.opp-lat1')
        self.assertEqual(scheme_grouper(text, text.getReffs), level_grouper(text, text.getReffs, 1, 2))

    def test_book_poem_line(self):
        """ Tests a text with book, poem, and line citations
        """
        text = NautilusDummy.getTextualNode('urn:cts:latinLit:phi1294.phi002.perseus-lat2')
        self.assertEqual(scheme_grouper(text, text.getReffs), level_grouper(text, text.getReffs, 2, 1))

    def test_book_line(self):
        """ Tests a text with book and line citations
        """
        text = NautilusDummy.getTextualNode('urn:cts:latinLit:phi1020.phi001.perseus-lat2')
        self.assertEqual(scheme_grouper(text, text.getReffs), level_grouper(text, text.getReffs, 2, 30))

    def test_book_chapter(self):
        """ Tests a text with book and chapter citations
        """
        text = NautilusDummy.getTextualNode('urn:cts:latinLit:phi1351.phi004.perseus-lat2')
        self.assertEqual(scheme_grouper(text, text.getReffs), level_grouper(text, text.getReffs, 2, 1))

    def test_book(self):
        """ Tests a text with book citations
        """
        text = NautilusDummy.getTextualNode('urn:cts:latinLit:stoa0149b.stoa006.opp-lat1')
        self.assertEqual(scheme_grouper(text, text.getReffs), level_grouper(text, text.getReffs, 1, 1))

    def test_line(self):
        """ Tests a text with line citations
        """
        text = NautilusDummy.getTextualNode('urn:cts:latinLit:phi0134.phi001.perseus-lat2')
        self.assertEqual(scheme_grouper(text, text.getReffs), level_grouper(text, text.getReffs, 1, 30))

    def test_chapter_section(self):
        """ Tests a text with chapter and section citations
        """
        text = NautilusDummy.getTextualNode('urn:cts:latinLit:stoa0275.stoa027.perseus-lat2')
        self.assertEqual(scheme_grouper(text, text.getReffs), level_grouper(text, text.getReffs, 2, 2))

    def test_chapter_mishnah(self):
        """ Tests a text with chapter and mishnah citations
        """
        text = NautilusDummy.getTextualNode('urn:cts:ancJewLit:mishnah.arakhin.p179204')
        self.assertEqual(scheme_grouper(text, text.getReffs), level_grouper(text, text.getReffs, 2, 1))

    def test_chapter_verse(self):
        """ Tests a text with chapter and verse citations
        """
        text = NautilusDummy.getTextualNode('urn:cts:ancJewLit:hebBible.leviticus.leningrad-pntd')
        self.assertEqual(scheme_grouper(text, text.getReffs), level_grouper(text, text.getReffs, 2, 1))

    def test_with_line(self):
        """ Tests a text with line citations mixed with something else
        """
        text = NautilusDummy.getTextualNode('urn:cts:latinLit:phi0690.phi003.perseus-lat2')
        self.assertEqual(scheme_grouper(text, text.getReffs), level_grouper(text, text.getReffs, 2, 30))

tic = CtsTextInventoryCollection()
latin = XmlCtsTextInventoryMetadata("urn:perseus:latinLit")
latin.parent = tic
latin.set_label("Classical Latin", "eng")
farsi = XmlCtsTextInventoryMetadata("urn:perseus:farsiLit")
farsi.parent = tic
farsi.set_label("Farsi", "eng")
gc = XmlCtsTextInventoryMetadata("urn:perseus:greekLit")
gc.parent = tic
gc.set_label("Ancient Greek", "eng")
gc.set_label("Grec Ancien", "fre")
heb = XmlCtsTextInventoryMetadata("urn:perseus:ancJewLit")
heb.parent = tic
heb.set_label("Hebrew", "eng")

dispatcher = CollectionDispatcher(tic)


@dispatcher.inventory("urn:perseus:latinLit")
def dispatchLatinLit(collection, path=None, **kwargs):
    if collection.id.startswith("urn:cts:latinLit:"):
        return True
    return False


@dispatcher.inventory("urn:perseus:farsiLit")
def dispatchfFarsiLit(collection, path=None, **kwargs):
    if collection.id.startswith("urn:cts:farsiLit:"):
        return True
    return False

@dispatcher.inventory("urn:perseus:ancJewLit")
def dispatchHebrewLit(collection, path=None, **kwargs):
    if collection.id.startswith("urn:cts:ancJewLit:"):
        return True
    return False

NautilusDummy = CtsCapitainsLocalResolver(
    resource=[
        "./tests/test_data/nautilus/hebLit",
        "./tests/test_data/nautilus/farsiLit",
        "./tests/test_data/nautilus/latinLit"
    ],
    dispatcher=dispatcher
)
NautilusDummy.logger.disabled = True
