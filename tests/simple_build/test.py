import os
from fileflood import Flood
from tests import FunctionalTest

class Test(FunctionalTest):

    def test(self):

        app = Flood(os.path.dirname(__file__))

        for page in app.find('*.html'):
            if page.path != 'index.html':
                root, ext = os.path.splitext(page.path)
                page.path = root + '/' + 'index.html'

        app.build()

        self.compare(app)
