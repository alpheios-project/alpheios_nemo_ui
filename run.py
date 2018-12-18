from tests.test_resources import NautilusDummy
from pkg_resources import resource_filename
from alpheios_nemo_ui import AlpheiosNemoUI, scheme_grouper
from flask_nemo import Nemo
from flask_nemo.chunker import level_grouper
from flask import Flask

app = Flask("Nemo")
app.debug = True
nemo = Nemo(
    app=app,
    GTrackCode="UA-8210342-1",
    base_url="",
    resolver=NautilusDummy,
    chunker={"default": scheme_grouper},
    plugins=[AlpheiosNemoUI("HERE")],
    transform={
        "default": resource_filename("alpheios_nemo_ui", "data/assets/static/xslt/epidocShort.xsl")
    }
)

if __name__ == "__main__":
    app.run()
