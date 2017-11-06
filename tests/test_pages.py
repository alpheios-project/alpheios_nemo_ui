"""
    Test the Nautilus endpoint with the app.test_client
"""
from unittest import TestCase
from tests.test_resources import NautilusDummy
from flask_nemo import Nemo
from flask_nemo.chunker import level_grouper
from flask import Flask, jsonify
from pkg_resources import resource_filename
from alpheios_nemo_ui import AlphieosNemoUI


class NemoTestBrowse(TestCase):
    """ Test Suite for Nemo
    """
    def make_nemo(self, app, **kwargs):
        return Nemo(app=app, **kwargs)

    def setUp(self):
        app = Flask("Nemo")
        app.debug = True
        self.nemo = self.make_nemo(
            app=app,
            base_url="",
            resolver=NautilusDummy,
            chunker={"default": lambda x, y: level_grouper(x, y, groupby=30)},
            plugins=[AlpheiosNemoUI("123google")],
            transform={
                "default": resource_filename("alpheios_nemo_ui", "data/assets/static/xslt/epidocShort.xsl")
            },
        )

        self.client = app.test_client()

    def test_default_template_assets(self):
        """ Test that the index menu is correctly built """
        query_data = self.client.get("/").data.decode()

        jss = []

        assert_length_js = len(jss)
        for js in jss:
            self.assertIn(
                '<script src="{0}"></script>'.format(js), query_data,
                "Templates should correctly link external js"
            )
            assert_length_js -= 1
        self.assertEqual(assert_length_js, 0, "All js file should have been checked")

        csss = [
            "/assets/nemo.secondary/css/theme-ext.css"
        ]
        assert_length_js = len(csss)
        for css in csss:
            self.assertIn(
                '<link rel="stylesheet" href="{0}">'.format(css), query_data,
                "Templates should correctly link external css"
            )
            assert_length_js -= 1
        self.assertEqual(assert_length_js, 0, "All css files should have been checked")

    def test_serving_primary_assets(self):
        """ Ensure primary assets are served
        """
        query_data = str(self.client.get("/assets/nemo/css/theme.min.css").data)
        self.assertIn("body, html", query_data, "Primary Assets should be served")

    def test_index_menu(self):
        """ Test that the index menu is correctly built """
        query_data = str(self.client.get("/").data)
        self.assertIn(
            '<a href="/collections/urn:perseus:farsiLit/farsi">Farsi</a>', query_data,
            "App should have link to farsiLit through local repository-endpoint object"
        )
        self.assertIn(
            '<a href="/collections/urn:perseus:latinLit/classical-latin">Classical Latin</a>', query_data,
            "App should have link to latinLit through local repository-endpoint object"
        )

    def test_namespace_page(self):
        """ Test that the namespace page has correct informations : """
        query_data = self.client.get("/collections/urn:perseus:farsiLit").data.decode()
        self.assertIn(
            '<a href="/collections/urn:perseus:farsiLit/farsi">Farsi</a>', query_data,
            "App should have link to farsiLit through local repository-endpoint object"
        )
        self.assertRegex(
            query_data,
            r'href="/collections/urn:cts:farsiLit:hafez/[\w\-]+">Browse \(1\)</a>',
            "App should have link to authors through local repository-endpoint object"
        )

    def test_author_page(self):
        """ Test that author page contains what is relevant : editions and translations """
        query_data = self.client.get("/collections/urn:cts:latinLit:phi1294").data.decode()
        self.assertIn(
            '<a href="/collections/urn:perseus:farsiLit/farsi">Farsi</a>', query_data,
            "App should have link to farsiLit through local repository-endpoint object"
        )
        self.assertRegex(
            query_data,
            r'href="/collections/urn:cts:latinLit:phi1294.phi002/[\w\-]+">Browse \(1\)</a>',
            "App should have link to the text object"
        )

    def test_author_page_more_count(self):
        """ Test that the namespace page has correct informations : """
        query_data = self.client.get("/collections/urn:cts:farsiLit:hafez").data.decode()
        self.assertIn(
            '<a href="/collections/urn:perseus:farsiLit/farsi">Farsi</a>', query_data,
            "App should have link to farsiLit through local repository-endpoint object"
        )
        self.assertRegex(
            query_data,
            r'href="/collections/urn:cts:farsiLit:hafez.divan/[\w\-]+">Browse \(3\)</a>',
            "App should have link to authors through local repository-endpoint object"
        )

    def test_text_page(self):
        """ Test that text page contains what is relevant : passages"""
        query_data = self.client.get("/text/urn:cts:latinLit:phi1294.phi002.perseus-lat2/references").data.decode()
        self.assertIn(
            '<a href="/collections/urn:perseus:farsiLit/farsi">Farsi</a>', query_data,
            "App should have link to farsiLit through local repository-endpoint object"
        )
        self.assertIn(
            '<a href="/text/urn:cts:latinLit:phi1294.phi002.perseus-lat2/passage/1.pr.1-1.pr.22">', query_data,
            "App should have link to farsiLit through local repository-endpoint object"
        )

    def test_passage_page(self):
        """ Test that passage page contains what is relevant : text and next passages"""
        query_data = str(self.client.get("/text/urn:cts:latinLit:phi1294.phi002.perseus-lat2/passage/1.pr.1-1.pr.22").data)
        self.assertIn(
            'Marsus, sic Pedo, sic Gaetulicus, sic quicumque perlegi', query_data,
            "Text should be visible"
        )
        self.assertIn(
            'href="/text/urn:cts:latinLit:phi1294.phi002.perseus-lat2/passage/1.1.1-1.1.6"', query_data,
            "App should have link to the next passage"
        )

    def test_json_route(self):
        """ Test that adding routes to Nemo instance (without plugin) which output json works
        """
        import json
        test_data = {"SomeDict": "IsGood"}

        class NemoJson(Nemo):
            ROUTES = Nemo.ROUTES + [("/getJson", "r_json", ["GET"])]

            def r_json(self):
                """ Route with no templates should return none as first value
                """
                return jsonify(test_data)

        app = Flask("Nemo")
        app.debug = True
        nemo = NemoJson(app=app, base_url="", resolver=NautilusDummy)
        client = app.test_client()
        query_data = json.loads(client.get("/getJson").data.decode('utf8'))

        self.assertEqual(
            query_data, test_data,
            "Original Dict and Decoded Output JSON should be equal"
        )

    def test_breadcrumb(self):
        """ Ensure breadcrumb is bydefault loaded
        """
        query_data = str(self.client.get("/collections/urn:cts:latinLit:phi1294").data)
        self.assertIn(
            '<li class="breadcrumb-item"><a href="/collections/urn:perseus:latinLit/classical-latin">Classical Latin</a></li>', query_data,
            "Breadcrumb should be visible"
        )
        self.assertIn(
            '<li class="breadcrumb-item active">Martial</li>', query_data,
            "Breadcrumb should be visible"
        )

    def test_no_default_breadcrumb(self):
        """ Ensure breadcrumb is bydefault loaded
        """

        app = Flask("Nemo")
        app.debug = True
        nemo = self.make_nemo(app=app, base_url="", resolver=NautilusDummy, original_breadcrumb=False)
        client = app.test_client()
        query_data = str(client.get("/collections/urn:cts:latinLit:phi1294").data)
        self.assertNotIn(
            '<ol class="breadcrumb">', query_data,
            "Breadcrumb should not be visible"
        )
        self.assertNotIn(
            '<li class="active">Martial</li>', query_data,
            "Breadcrumb should not be visible"
        )

    def test_main_collections(self):
        """ Test the main collection (Inventory) display
        """
        query_data = self.client.get("/collections").data.decode()
        self.assertRegex(
            query_data, "Classical Latin<br />\s*<a class=\"card-link\" href=\"/collections/urn:perseus:latinLit",
            "Link to classical latin main collection should be found"
        )
        self.assertRegex(
            query_data, "Farsi<br />\s*<a class=\"card-link\" href=\"/collections/urn:perseus:farsiLit",
            "Link to farsi main collection should be found"
        )
        self.assertRegex(
            query_data, "Ancient Greek<br />\s*<a class=\"card-link\" href=\"/collections/urn:perseus:greekLit",
            "Link to farsi main collection should be found"
        )

    def test_semantic_collections(self):
        """ Test the main collection (Inventory) display
        """
        query_data = self.client.get("/collections/urn:perseus:latinLit/something").data.decode()
        query_data_2 = self.client.get("/collections/urn:perseus:latinLit").data.decode()
        self.assertEqual(
            query_data, query_data_2, "Semantic has no effect on output"
        )

    def test_i18n_metadata(self):
        """ Ensure metadata are i18n according to requested headers
        """
        tests = [
            ("en_US", "I am English."),
            ("fr_CA", "Je suis francais."),
            ("fr_FR", "Je suis francais."),
            ("la", "Ego romanus sum."),
            ("de_DE", "Ich bin Deutsch.")
        ]
        ran = 0
        for lang, text in tests:
            data = self.client.get(
                "/collections/urn:cts:latinLit:phi1318.phi001",
                headers=[("Accept-Language", lang)]
            ).data.decode()
            self.assertIn(
                text, data
            )
            ran += 1
        self.assertEqual(ran, len(tests), "There should be as much ran tests as there is tests")

    def test_first_passage(self):
        tests = 0
        uris = [
            ("urn:cts:latinLit:phi1294.phi002.perseus-lat2", "1.pr.1-1.pr.20"),
            ("urn:cts:latinLit:phi1318.phi001.perseus-unk2", "8.pr.1-8.pr.20"),
            ("urn:cts:farsiLit:hafez.divan.perseus-ger1", "1.1.1.1-1.1.1.4")
        ]
        app = Flask("Nemo")
        _ = self.make_nemo(
            app=app,
            base_url="",
            resolver=NautilusDummy,
            original_breadcrumb=False,
            chunker={"default": lambda x, y: level_grouper(x, y, groupby=20)}
        )
        client = app.test_client()
        for oId, psg in uris:
            r = client.get("/text/{}/passage".format(oId))
            self.assertIn(
                "/text/{}/passage/{}/".format(oId, psg), r.location,
                "check that the path changed"
            )
            tests += 1
        self.assertEqual(tests, len(uris), "There should be as much ran tests as there is tests")

    def test_no_siblings_is_ok(self):
        """ Test that passage page contains what is relevant : text and next passages"""
        query_data = self.client.get("/text/urn:cts:latinLit:stoa0329c.stoa001.opp-lat1/passage/1-8").data.decode()
        self.assertIn(
            'et ibi est lapis ille', query_data,
            "Text should be visible"
        )

    def test_assert_analytics(self):
        """ Test that passage page contains what is relevant : text and next passages"""
        query_data = self.client.get("/text/urn:cts:latinLit:stoa0329c.stoa001.opp-lat1/passage/1-8").data.decode()
        self.assertIn(
            "ga('create', '123google', 'auto');", query_data,
            "Google Analytics ID should be shown"
        )
