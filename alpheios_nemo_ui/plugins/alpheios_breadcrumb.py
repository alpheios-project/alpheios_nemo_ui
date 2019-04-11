# -*- coding: utf-8 -*-

from flask_nemo.plugin import PluginPrototype
from flask_nemo.filters import f_slugify
from pkg_resources import resource_filename
from MyCapytain.common.reference import URN
import sys


class AlpheiosBreadcrumb(PluginPrototype):
    """
        Alpheios Breadcrumb

    """
    HAS_AUGMENT_RENDER = True
    TEMPLATES = {"main": resource_filename("alpheios_nemo_ui", "data/templates_plugins/breadcrumb")}

    def render(self, **kwargs):
        """ Make breadcrumbs for a route

        :param kwargs: dictionary of named arguments used to construct the view
        :type kwargs: dict
        :return: List of dict items the view can use to construct the link.
        :rtype: {str: list({ "link": str, "title", str, "args", dict})}
        """
        breadcrumbs = []
        # this is the list of items we want to accumulate in the breadcrumb trail.
        # item[0] is the key into the kwargs["url"] object and item[1] is the  name of the route
        # setting a route name to None means that it's needed to construct the route of the next item in the list
        # but shouldn't be included in the list itself (this is currently the case for work --
        # at some point we probably should include work in the navigation)
        breadcrumbs = []
        menu = []
        if "collections" in kwargs:
            breadcrumbs = [{
                "title": "Language",
                "link": ".r_collections",
                "args": {}
            }]
            menu = [{
                "title": "Language",
                "link": ".r_collections",
                "args": {}
            }]

            if "parents" in kwargs["collections"]:
                breadcrumbs += [
                    {
                        "title": self.get_title(parent["class"]),
                        "link": ".r_collection",
                        "args": {
                            "objectId": parent["id"],
                        },
                    } for parent in kwargs["collections"]["parents"]
                ][::-1]
                menu += [
                    {
                        "title": self.get_title(parent["class"]),
                        "current": parent["label"],
                        "link": ".r_collection",
                        "args": {
                            "objectId": parent["id"],
                        },
                    } for parent in kwargs["collections"]["parents"]
                ][::-1]

            if "current" in kwargs["collections"]:
                if (kwargs["collections"]["current"]["model"] == 'http://w3id.org/dts-ontology/resource'):
                    if ('citation' in kwargs["collections"]["current"]):
                        title = "Read"
                    else:
                        title = "Browse"
                    breadcrumbs.append({
                        "title": title,
                        "link": None,
                        "args": {}
                    })
                else:
                    breadcrumbs.append({
                        "title": self.get_title(kwargs["collections"]["current"]["class"]),
                        "link": None,
                        "args": {}
                    })

        # don't link the last item in the trail
        if len(breadcrumbs) > 0:
            breadcrumbs[-1]["link"] = None

        return {"breadcrumbs": breadcrumbs, "menu": menu}

    def get_title(self,classname):
        if classname == 'XmlCtsTextgroupMetadata':
            return 'Works'
        elif classname == 'XmlCtsTextInventoryMetadata':
            return 'Authors'
        elif classname == 'CtsTextInventoryMetadata':
            return 'Authors'
        else:
            return classname



