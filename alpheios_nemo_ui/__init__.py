# -*- coding: utf-8 -*-

from flask_nemo.plugin import PluginPrototype
from pkg_resources import resource_filename
from flask import jsonify, url_for
from flask_nemo.chunker import level_grouper
import re


class AlpheiosNemoUI(PluginPrototype):
    """
        The Breadcrumb plugin is enabled by default in Nemo.
        It can be overwritten or removed. It simply adds a breadcrumb

    """
    HAS_AUGMENT_RENDER = False
    TEMPLATES = {
        "main": resource_filename("alpheios_nemo_ui", "data/templates/main"),
        "alpheios": resource_filename("alpheios_nemo_ui", "data/templates/alpheios")
    }
    CSS = [
     resource_filename("alpheios_nemo_ui", "data/assets/css/alpheios.min.css"),
     resource_filename("alpheios_nemo_ui", "data/assets/css/style.min.css"),
     resource_filename("alpheios_nemo_ui", "data/assets/css/style-embedded.min.css")
    ]
    JS = [
        resource_filename("alpheios_nemo_ui", "data/assets/js/bloodhound.min.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/autocomplete.min.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/menu.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/text.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/mobile.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/alpheios-embedded.js")
    ]
    STATICS = [
        resource_filename("alpheios_nemo_ui", "data/assets/images/logo.png")
    ]
    ROUTES = [
        ("/typeahead/collections.json", "r_typeahead_json", ["GET"])
    ]

    CACHED = ["r_typeahead_json"]
    HAS_AUGMENT_RENDER = True

    def __init__(self, GTrackCode=None, *args, **kwargs):
        super(AlpheiosNemoUI, self).__init__(*args, **kwargs)
        self.GTrackCode = GTrackCode

    def render(self, **kwargs):
        kwargs["gtrack"] = self.GTrackCode
        # this is a hack to enable inclusion of the language code in the top html
        # element of the page for backwards compatibility with Alpheios V1 which
        # looks for the language of pedagogical texts there
        # it only works for cts texts with edition naming scheme which ends in <lang>\d
        # (e.g. alpheios-text-grc1)
        if ("objectId" in kwargs):
            kwargs["lang"] = re.sub(r"^.*?-(\w\w\w)\d$", r"\1", kwargs["objectId"])
        else:
            kwargs["lang"] = 'en'
        return kwargs

    def r_typeahead_json(self):
        """ List of resource for typeahead
        """

        locale = self.nemo.get_locale()
        collection = self.nemo.resolver.getMetadata()
        data = []
        for collection in collection.readableDescendants:
            parents = ", ".join([str(p.get_label(locale)) for p in collection.parents if p.get_label(locale)])
            title = str(collection.get_label(locale))
            desc = collection.get_description(locale)
            if desc is not None:
                desc = str(desc)
            else:
                desc = ""
            data.append({
                "value": title + ", " + parents + desc,
                "title": title,
                "parents": parents,
                #"description": desc,
                "uri": url_for(".r_first_passage", objectId=str(collection.id))
            })
        return jsonify(data)


def scheme_grouper(text, getreffs):
    level = len(text.citation)
    groupby = 5
    types = [citation.name for citation in text.citation]

    if 'word' in types:
        types = types[:types.index("word")]
    if str(text.id) == "urn:cts:latinLit:stoa0040.stoa062.opp-lat1":
        level, groupby = 1, 2
    elif types == ["book", "poem", "line"]:
        level, groupby = 2, 1
    elif types == ["book", "line"]:
        level, groupby = 2, 30
    elif types == ["book", "chapter"]:
        level, groupby = 2, 1
    elif types == ["book"]:
        level, groupby = 1, 1
    elif types == ["line"]:
        level, groupby = 1, 30
    elif types == ["chapter", "section"]:
        level, groupby = 2, 2
    elif types == ["chapter", "mishnah"]:
        level, groupby = 2, 1
    elif types == ["chapter", "verse"]:
        level, groupby = 2, 1
    elif types == ["book", "page"]:
        level, groupby = 2, 1
    elif "line" in types:
        groupby = 30
    return level_grouper(text, getreffs, level, groupby)
