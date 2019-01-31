# -*- coding: utf-8 -*-

import os
from flask import Flask, request
from werkzeug.contrib.cache import RedisCache, FileSystemCache
from flask_caching import Cache
from pkg_resources import resource_filename

from MyCapytain.resources.prototypes.cts.inventory import CtsTextInventoryCollection as TextInventoryCollection, CtsTextInventoryMetadata as PrototypeTextInventory
from MyCapytain.resolvers.utils import CollectionDispatcher
from capitains_nautilus.cts.resolver import NautilusCTSResolver

from flask_nemo import Nemo
from flask_nemo.chunker import level_grouper
from capitains_nautilus.flask_ext import FlaskNautilus
from alpheios_nemo_ui import AlpheiosNemoUI, scheme_grouper

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
def dispatchGreekLit(collection, path=None, **kwargs):
    if collection.id.startswith("urn:cts:arabicLit:"):
        return True
    return False

@dispatcher.inventory("urn:perseus:greekLit")
def dispatchGreekLit(collection, path=None, **kwargs):
    if collection.id.startswith("urn:cts:greekLit:"):
        return True
    return False

resolver = NautilusCTSResolver(
    [os.path.join(d,o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))],
    dispatcher=dispatcher,
    cache=nautilus_cache
)

app = Flask("Nautilus")
nautilus = FlaskNautilus(
    app=app,
    prefix="/api",
    name="nautilus",
    resolver=resolver,
    flask_caching=http_cache
)
nautilus_api = FlaskNautilus(prefix="/api", app=app, resolver=resolver)


# We set up Nemo
nemo = Nemo(
    app=app,
    name="nemo",
    base_url="",
    cache=http_cache,
    resolver=resolver,
    chunker={
        "default": scheme_grouper
    },
    plugins=[AlpheiosNemoUI("UA-8210342-1")],
    transform={
        "default": resource_filename("alpheios_nemo_ui","data/assets/static/xslt/alpheios-enhanced.xsl")
    },

)
http_cache.init_app(app)
#app.debug = True

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
