# -*- coding: utf-8 -*-

import os
import sys
from flask import Flask, request
from flask_assets import Environment, Bundle
from webassets.filter import get_filter
from werkzeug.contrib.cache import RedisCache, FileSystemCache
from flask_caching import Cache
from pkg_resources import resource_filename

from MyCapytain.common.reference import URN
from MyCapytain.resources.prototypes.cts.inventory import CtsTextInventoryCollection as TextInventoryCollection, CtsTextInventoryMetadata as PrototypeTextInventory
from MyCapytain.resolvers.utils import CollectionDispatcher
from capitains_nautilus.cts.resolver import NautilusCTSResolver

from flask_nemo import Nemo
from flask_nemo.chunker import level_grouper
from capitains_nautilus.flask_ext import FlaskNautilus
from alpheios_nemo_ui import AlpheiosNemoUI, scheme_grouper
from alpheios_nemo_ui.plugins.alpheios_breadcrumb import AlpheiosBreadcrumb

d = "/home/balmas/workspace/cts_test"
#
tic = TextInventoryCollection()
latin = PrototypeTextInventory("urn:perseus:latinLit", parent=tic)
latin.set_label("Classical Latin", "eng")
latin.set_label("Latin Classique", "fre")
ara = PrototypeTextInventory("urn:alpheios:arabicLit", parent=tic)
ara.set_label("Classical Arabic", "eng")
ara.set_label("Arabe Classique", "fre")
gc = PrototypeTextInventory("urn:perseus:greekLit", parent=tic)
gc.set_label("Ancient Greek", "eng")
gc.set_label("Grec Ancien", "fre")

http_cache = Cache(config={'CACHE_TYPE': "redis", "CACHE_REDIS_HOST": "localhost", "CACHE_DEFAULT_TIMEOUT": 0})
#nautilus_cache = RedisCache("localhost", port=6379, default_timeout=0)
#http_cache = Cache(config={'CACHE_TYPE': "filesystem", "CACHE_DIR": "<%= scope.lookupvar('capitains::cache_dir') %>", "CACHE_DEFAULT_TIMEOUT": 28800})
nautilus_cache = FileSystemCache("/tmp/ctscache", threshold=10000, default_timeout=28800)
dispatcher = CollectionDispatcher(tic)



@dispatcher.inventory("urn:perseus:latinLit")
def dispatchLatinLit(collection, path=None, **kwargs):
    if collection.id.startswith("urn:cts:latinLit:"):
        return True
    return False

@dispatcher.inventory("urn:alpheios:arabicLit")
def dispatchArabicLit(collection, path=None, **kwargs):
    if collection.id.startswith("urn:cts:arabicLit:"):
        return True
    return False

@dispatcher.inventory("urn:perseus:greekLit")
def dispatchGreekLit(collection, path=None, **kwargs):
    if collection.id.startswith("urn:cts:greekLit:"):
        return True
    return False

unfiltered_collections = {
    'arabicLit': 1,
}

allowed_textgroups = [
    'phi0893', # Horace
    'phi0474', # Cicero
    'tlg0011', # Sophocles
]

allowed_works = [
    'urn:cts:latinLit:phi0690.phi003', # vergil aen id
    'urn:cts:latinLit:phi0448.phi001', # caesar gallic war
    'urn:cts:latinLit:phi0472.phi001', # catullus carmina
    'urn:cts:latinLit:phi0620.phi001', # propertius elegies
    'urn:cts:greekLit:tlg0020.tlg001', # hesiod theogeny
    'urn:cts:greekLit:tlg0020.tlg003', # hesiod shield
    'urn:cts:greekLit:tlg0032.tlg006', # xenophon anabasis
    'urn:cts:greekLit:tlg0032.tlg007', # xenophon cyropaedia
    'urn:cts:greekLit:tlg0032.tlg001', # xenophon hellenica
    'urn:cts:greekLit:tlg0032.tlg002', # xenophon memorabilia
]

allowed_editions = [
    'urn:cts:latinLit:phi0959.phi006.alpheios-text-lat1',
    'urn:cts:greekLit:tlg0085.tlg003.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0085.tlg004.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0085.tlg007.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0085.tlg006.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0085.tlg002.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0085.tlg005.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0085.tlg001.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0012.tlg001.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0012.tlg002.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0020.tlg003.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0020.tlg002.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0020.tlg001.alpheios-text-grc1',
    'urn:cts:greekLit:tlg0011.tlg003.alpheios-text-grc1',
]

excluded_editions = [
    'urn:cts:greekLit:tlg0011.tlg003.perseus-grc2',
]

resolver = NautilusCTSResolver(
    [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))],
    dispatcher=dispatcher,
    filter = lambda t: (t.__subtype__ == 'edition' and t.urn.upTo(URN.VERSION) not in excluded_editions and (str(t.urn.namespace) in unfiltered_collections or str(t.urn.textgroup) in allowed_textgroups or t.urn.upTo(URN.WORK) in allowed_works or t.urn.upTo(URN.VERSION) in allowed_editions)),
    cache=None
)

app = Flask("Nautilus")
nautilus = FlaskNautilus(
    app=app,
    prefix="/api",
    name="nautilus",
    resolver=resolver,
    flask_caching=None
)

# We set up Nemo
nemo = Nemo(
    app=app,
    name="nemo",
    base_url="",
    cache=None,
    resolver=resolver,
    chunker={
        "default": scheme_grouper
    },
    original_breadcrumb = False,
    plugins=[AlpheiosNemoUI(""),AlpheiosBreadcrumb()],
    transform={
        "default": resource_filename("alpheios_nemo_ui","data/assets/static/xslt/alpheios-enhanced.xsl")
    },
)

http_cache.init_app(app)
#app.debug = True

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
