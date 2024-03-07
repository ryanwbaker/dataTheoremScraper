import falcon
from .api import Resource

app = application = falcon.App()

api = Resource()
app.add_route('/api', api)
