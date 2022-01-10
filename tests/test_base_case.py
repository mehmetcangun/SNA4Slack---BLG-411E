import unittest
from server import create_app
from src.models.DB import db
from src.models.Users import User
from flask import template_rendered, url_for

from contextlib import contextmanager
class BaseTestCase(unittest.TestCase):
    """
    Reference: https://github.com/allisson/flask-example/blob/master/common/tests.py
    """
    def __call__(self, result = None):
        self._pre_set_up()
        super(BaseTestCase, self).__call__(result)
        self._post_tear_down()
    
    def _pre_set_up(self):
        self.app = create_app("config_test")
        self.client = self.app.test_client()
        self.ctx = self.app.test_request_context()
        self.ctx.push()
        db.create_all()

    def _post_tear_down(self):
        db.drop_all()
        #db.session.close()
        self.ctx.pop()
    
    @contextmanager
    def captured_templates(self, app):
        recorded = []

        def record(sender, template, context, **extra):
            recorded.append((template, context))

        template_rendered.connect(record, app)

        try:
            yield recorded
        finally:
            template_rendered.disconnect(record, app)
    
    
class TestWebApp(BaseTestCase):

    def test_home_page(self):
        response = self.client.get(url_for("upload_page"))
        self.assertEqual(response.status_code, 200)

    def test_db_query(self):
        
        qry = db.session.query(User).count()
        self.assertEqual(qry, 0)
