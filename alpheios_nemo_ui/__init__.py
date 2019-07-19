# -*- coding: utf-8 -*-

from flask_nemo.plugin import PluginPrototype
from pkg_resources import resource_filename
from flask import jsonify, url_for, redirect, Markup, session, request, send_from_directory, make_response
from flask_nemo.chunker import level_grouper
from copy import deepcopy as copy
import re
import collections

from MyCapytain.common.constants import RDF_NAMESPACES, Mimetypes
from MyCapytain.resources.prototypes.metadata import ResourceCollection
from MyCapytain.resources.prototypes.cts.inventory import CtsWorkMetadata, CtsEditionMetadata
from MyCapytain.resources.collections.cts import XmlCtsTextgroupMetadata
from MyCapytain.errors import UnknownCollection
import sys
import alpheios_nemo_ui.filters
from rdflib import Namespace
from six.moves.urllib.parse import urlencode
from functools import wraps


class AlpheiosNemoUI(PluginPrototype):
    HAS_AUGMENT_RENDER = False
    TEMPLATES = {
        "main": resource_filename("alpheios_nemo_ui", "data/templates/main"),
        "alpheios": resource_filename("alpheios_nemo_ui", "data/templates/alpheios")
    }
    CSS = [
     resource_filename("alpheios_nemo_ui", "data/assets/css/alpheios.min.css"),
     resource_filename("alpheios_nemo_ui", "data/assets/node_modules/alpheios-components/dist/style/style-components.min.css"),

    ]
    JS = [
        resource_filename("alpheios_nemo_ui", "data/assets/js/bloodhound.min.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/autocomplete.min.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/menu.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/text.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/infinite-scroll.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/passage-search.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/browse.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/js/env.js"),
        # we need to include these here so that we can refer to the them in the templates using the nemo.secondary
        # abstract static url but they should be excluded from assets that get imported
        # via script tags because they should use dynamic imports
        resource_filename("alpheios_nemo_ui", "data/assets/node_modules/alpheios-embedded/dist/alpheios-embedded.min.js"),
        resource_filename("alpheios_nemo_ui", "data/assets/node_modules/alpheios-components/dist/alpheios-components.min.js")
    ]
    STATICS = [
        resource_filename("alpheios_nemo_ui", "data/assets/images/logo.png"),
        resource_filename("alpheios_nemo_ui", "data/assets/images/alpheios-logo.svg"),
        resource_filename("alpheios_nemo_ui", "data/assets/images/Alpheios-Logo-White.png"),
        resource_filename("alpheios_nemo_ui", "data/assets/images/Menu-Icon.svg"),
        resource_filename("alpheios_nemo_ui", "data/assets/images/Divider-Lg.svg"),
        resource_filename("alpheios_nemo_ui", "data/assets/images/Divider-Sm.svg")
    ]

    ROUTES = [
        ("/", "r_index", ["GET"]),
        ("/collections", "r_collections", ["GET"]),
        ("/collections/<objectId>", "r_collection", ["GET"]),
        ("/text/<objectId>/references", "r_references", ["GET"]),
        ("/text/<objectId>/passage/<subreference>", "r_passage", ["GET"]),
        ("/text/<objectId>/passage/<subreference>/json", "r_passage_json", ["GET"]),
        ("/text/<objectId>/passage", "r_first_passage", ["GET"]),
        ("/typeahead/collections.json", "r_typeahead_json", ["GET"]),
        ("/authorize","r_authorize",["GET"]),
        ("/login","r_login",["GET"]),
        ("/logout","r_logout",["GET"]),
        ("/return","r_logout_return",["GET"]),
        ("/userinfo","r_userinfo",["GET"]),
        ("/usertoken","r_usertoken",["GET"])
    ]

    FILTERS = [
        "f_hierarchical_passages_full",
        "f_i18n_citation_label",
        "f_i18n_citation_item",
        "f_citation_name",
        "f_i18n_readable_book_title",
        "f_citation_link"
    ]

    CACHED = ["r_typeahead_json"]
    HAS_AUGMENT_RENDER = True

    def __init__(self, GTrackCode=None, auth0=None, external_url_base='http://localhost:5000', *args, **kwargs):
        super(AlpheiosNemoUI, self).__init__(*args, **kwargs)
        self.GTrackCode = GTrackCode
        self.auth0 = auth0
        self.external_url_base = external_url_base
        self.clear_routes = True
        self.f_hierarchical_passages_full = filters.f_hierarchical_passages_full
        self.f_i18n_citation_label = filters.f_i18n_citation_label
        self.f_i18n_citation_item = filters.f_i18n_citation_item
        self.f_citation_name = filters.f_citation_name
        self.f_i18n_readable_book_title = filters.f_i18n_readable_book_title
        self.f_citation_link = filters.f_citation_link
        self._get_lang = _get_lang

    def r_index(self):
        """ Retrieve the top collections of the inventory

        :param lang: Lang in which to express main data
        :type lang: str
        :return: Collections information and template
        :rtype: {str: Any}
        """
        collection = self.nemo.resolver.getMetadata()
        return {
            "template": "alpheios::collection.html",
            "current_label": collection.get_label(None),
            "collections": {
                "members": self.nemo.make_members(collection, lang=None)
            }
        }

    def r_collections(self, lang=None):
        """ Retrieve the top collections of the inventory

        :param lang: Lang in which to express main data
        :type lang: str
        :return: Collections information and template
        :rtype: {str: Any}
        """
        collection = self.nemo.resolver.getMetadata()
        if collection:
            return {
                "template": "alpheios::collection.html",
                "current_label": collection.get_label(lang),
                "collections": {
                    "members": self.nemo.make_members(collection, lang=lang)
                }
            }
        else:
            return {
                "template": "alpheios::collection.html",
                "current_label": "NONE",
                "collections": {
                    "members": list()
                }
            }


    def r_collection(self, objectId, lang=None):
        """ Collection content browsing route function

        :param objectId: Collection identifier
        :type objectId: str
        :param lang: Lang in which to express main data
        :type lang: str
        :return: Template and collections contained in given collection
        :rtype: {str: Any}
        """
        collection = self.nemo.resolver.getMetadata(objectId)
        lang = self._get_lang(objectId,lang)
        members = self.nemo.make_members(collection, lang=lang)
        expanded_members = list()
        types = {}

        lettersSorted = collections.OrderedDict()
        DCT = Namespace("http://purl.org/dc/terms/")
        if isinstance(collection, XmlCtsTextgroupMetadata):
            for m in members:
                e_coll = self.nemo.resolver.getMetadata(m['id'])
                e =  {
                    "work": m,
                    "editions": self.nemo.make_members(e_coll,lang=lang)
                }
                workType = e_coll.metadata.get_single(DCT.type, lang)
                if workType is not None:
                    if workType not in types:
                        types[workType] = []
                    types[workType].append(e)
                else:
                    expanded_members.append(e)
        else:
            letters = {}
            for m in members:
                letter = m['label'][0]
                if letter not in letters:
                    letters[letter] = []
                letters[letter].append(m)

            for key in sorted(letters.keys()) :
                lettersSorted[key] = letters[key]

        return {
            "template": "alpheios::collection.html",
            "collections": {
                "current": {
                    "label": str(collection.get_label(lang)),
                    "label_lang": lang,
                    "id": collection.id,
                    "model": str(collection.model),
                    "type": str(collection.type),
                    "class": collection.__class__.__name__
                },
                "members": self.nemo.make_members(collection, lang=lang),
                "parents": self.make_parents(collection, lang=lang),
                "types": types,
                "letters": lettersSorted,
                "expanded_members": expanded_members
            },
        }

    def r_references(self, objectId, lang=None):
        """ Text exemplar references browsing route function

        :param objectId: Collection identifier
        :type objectId: str
        :param lang: Lang in which to express main data
        :type lang: str
        :return: Template and required information about text with its references
        """
        collection, reffs = self.nemo.get_reffs(objectId=objectId, export_collection=True)
        lang = self._get_lang(objectId,lang)
        cite = collection.citation
        scheme = []
        while (cite):
            scheme.append(cite.name)
            cite = cite.child
        return {
            "template": "alpheios::references.html",
            "objectId": objectId,
            "citation": collection.citation,
            "scheme": scheme,
            "collections": {
                "current": {
                    "label": collection.get_label(lang),
                    "label_lang": lang,
                    "id": collection.id,
                    "model": str(collection.model),
                    "type": str(collection.type),
                },
                "parents": self.make_parents(collection, lang=lang)
            },
            "reffs": reffs
        }

    def r_first_passage(self, objectId):
        """ Provides a redirect to the first passage of given objectId

        :param objectId: Collection identifier
        :type objectId: str
        :return: Redirection to the first passage of given text
        """
        collection, reffs = self.nemo.get_reffs(objectId=objectId, export_collection=True)
        first, _ = reffs[0]
        return redirect(
            url_for(".r_passage", objectId=objectId, subreference=first)
        )

    def r_passage(self, objectId, subreference, lang=None):
        """ Retrieve the text of the passage

        :param objectId: Collection identifier
        :type objectId: str
        :param lang: Lang in which to express main data
        :type lang: str
        :param subreference: Reference identifier
        :type subreference: str
        :return: Template, collections metadata and Markup object representing the text
        :rtype: {str: Any}
        """
        # keep track of the number of text views in a session to determine whether
        # or not to force a survey popup
        if 'textViews' in session:
            session['textViews'] = session['textViews'] + 1
        else:
            session['textViews'] = 1
        print(str(session),file=sys.stdout)
        collection = self.nemo.get_collection(objectId)
        lang = self._get_lang(objectId,lang)
        if isinstance(collection, CtsWorkMetadata):
            editions = [t for t in collection.children.values() if isinstance(t, CtsEditionMetadata)]
            if len(editions) == 0:
                raise UnknownCollection("This work has no default edition")
            return redirect(url_for(".r_passage", objectId=str(editions[0].id), subreference=subreference))
        text = self.nemo.get_passage(objectId=objectId, subreference=subreference)
        passage = self.nemo.transform(text, text.export(Mimetypes.PYTHON.ETREE), objectId)
        prev, next = self.nemo.get_siblings(objectId, subreference, text)
        newLevel = self.new_level(subreference,prev)
        return {
            "template": "main::text.html",
            "objectId": objectId,
            "subreference": subreference,
            "new_level": newLevel,
            "collections": {
                "current": {
                    "label": collection.get_label(lang),
                    "label_lang": lang,
                    "id": collection.id,
                    "model": str(collection.model),
                    "type": str(collection.type),
                    "author": text.get_creator(lang),
                    "title": text.get_title(lang),
                    "title_lang": lang,
                    "description": text.get_description(lang),
                    "citation": collection.citation,
                    "coins": self.nemo.make_coins(collection, text, subreference, lang=lang)
                },
                "parents": self.make_parents(collection, lang=lang)
            },
            "text_passage": Markup(passage),
            "prev": prev,
            "next": next
        }

    def r_passage_json(self, objectId, subreference, lang=None):
        """ Retrieve the text of the passage

        :param objectId: Collection identifier
        :type objectId: str
        :param lang: Lang in which to express main data
        :type lang: str
        :param subreference: Reference identifier
        :type subreference: str
        :return: Template, collections metadata and Markup object representing the text
        :rtype: {str: Any}
        """
        collection = self.nemo.get_collection(objectId)
        lang = self._get_lang(objectId,lang)
        if isinstance(collection, CtsWorkMetadata):
            editions = [t for t in collection.children.values() if isinstance(t, CtsEditionMetadata)]
            if len(editions) == 0:
                raise UnknownCollection("This work has no default edition")
            return redirect(url_for(".r_passage_json", objectId=str(editions[0].id), subreference=subreference))
        text = self.nemo.get_passage(objectId=objectId, subreference=subreference)
        passage = self.nemo.transform(text, text.export(Mimetypes.PYTHON.ETREE), objectId)
        prev, next = self.nemo.get_siblings(objectId, subreference, text)
        newLevel = self.new_level(subreference,prev)

        nextUrl = None
        if next:
            nextUrl = url_for('.r_passage', objectId=objectId, subreference=next)
        data = {
            "objectId": objectId,
            "subreference": subreference,
            "new_level": newLevel,
            "nextUrl": nextUrl,
            "collections": {
                "current": {
                    "label": collection.get_label(lang),
                    "id": collection.id,
                    "model": str(collection.model),
                    "type": str(collection.type),
                    "author": text.get_creator(lang),
                    "title": text.get_title(lang),
                    "description": text.get_description(lang),
                    "coins": self.nemo.make_coins(collection, text, subreference, lang=lang)
                },
                "parents": self.make_parents(collection, lang=lang)
            },
            "text_passage": Markup(passage),
            "prev": prev,
            "next": next
        }
        return jsonify(data)

    def r_assets(self, filetype, asset):
        """ Route for specific assets.

        :param filetype: Asset Type
        :param asset: Filename of an asset
        :return: Response
        """
        if filetype in self.nemo.assets and asset in self.nemo.assets[filetype] and self.nemo.assets[filetype][asset]:
            return send_from_directory(
                directory=self.nemo.assets[filetype][asset],
                filename=asset
            )
        abort(404)

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

    @property
    def clear_routes(self):
       pass

    def clear_routes(self,value):
      self.clear_routes = value


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

    def r_authorize(self):
        # Handles response from token endpoint
        tokens = self.auth0.authorize_access_token()
        # Store the access token in the flask session
        session['access_token'] = tokens['access_token']
        resp = self.auth0.get('userinfo')
        userinfo = resp.json()

        # Store the user information in flask session.
        session['jwt_payload'] = userinfo
        session['profile'] = {
            'sub': userinfo['sub'],
            'nickname': userinfo['nickname'],
        }
        if 'loginReturn' in session and session['loginReturn'] is not None:
            return redirect(session['loginReturn'])
        else:
            return redirect(url_for('.r_index'))

    def r_login(self):
        # Clear session stored data
        session.clear()
        session['loginReturn'] = request.args.get('next','')
        return self.auth0.authorize_redirect(redirect_uri=self.external_url_base + "/authorize",audience='alpheios.net:apis')

    def r_logout(self):
        # Clear session stored data
        session.clear()
        session['logoutReturn'] = request.args.get('next','')
        params = {'returnTo': self.external_url_base + '/return', 'client_id': self.auth0.client_id}
        return redirect(self.auth0.api_base_url + '/v2/logout?' + urlencode(params))

    def r_logout_return(self):
        if 'logoutReturn' in session and session['logoutReturn'] is not None:
            return redirect(session['logoutReturn'])
        else:
            return redirect(url_for('.r_index'))

    def requires_auth(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'profile' not in session:
                return "Unauthorized request", 401
            return f(*args, **kwargs)

        return decorated

    @requires_auth
    def r_userinfo(self):
        return jsonify(session['profile'])

    @requires_auth
    def r_usertoken(self):
        return jsonify(session['access_token'])

    def make_parents(self, collection, lang=None):
        """ Build parents list for given collection

        :param collection: Collection to build dict view of for its members
        :param lang: Language to express data in
        :return: List of basic objects
        """
        return [
            {
                "id": member.id,
                "label": str(member.get_label(lang)),
                "model": str(member.model),
                "type": str(member.type),
                "size": member.size,
                "class": member.__class__.__name__
            }
            for member in collection.parents
            if member.get_label()
        ]

    def new_level(self,subreference,prev):
        curr_first = subreference.split('-')[0]
        curr_levels = curr_first.split('.')
        if prev and len(curr_levels)>1:
            prev_first = prev.split('-')[0]
            prev_levels = prev_first.split('.')
            if len(prev_levels) == len(curr_levels) and curr_levels[-2] != prev_levels[-2]:
                curr_levels.pop()
                return '.'.join(curr_levels)
            else:
                return None
        elif len(curr_levels)>1:
            curr_levels.pop()
            return '.'.join(curr_levels)
        else:
            return None

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

def _get_lang(objectId,lang):
    if ('latin' in objectId):
        lang = 'lat'
    elif ('greek' in objectId):
        lang = 'grc'
    elif ('arabic' in objectId):
        lang = 'ara'
    elif ('persian' in objectId):
        lang = 'far'
    else:
        lang = lang or 'eng'
    return lang

