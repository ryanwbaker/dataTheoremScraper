import falcon # type: ignore
from .api import Resource

class StaticResource(object):
    def on_get(self, req, resp):
        # do some sanity check on the filename
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        with open('static/index.html', 'r') as f:
            resp.body = f.read()



app = application = falcon.App()

api = Resource()
app.add_route('/api', api)
app.add_route('/', StaticResource())
