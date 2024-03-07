import json
import falcon
from . import scraper


class Resource:

    def on_get(self, req, resp):
        # doc = {
        #     'app_name': 'App Name',
        #     'app_version': '1.0',
        #     'app_downloads': '2.5M',
        #     'release_date': '03-05-2024',
        #     'description': 'This is the description',
        # }

        # Parse query string
        # try:
        #     query_params = dict(req.params.items())
        #     app_data = scraper.AptoideApp(query_params['url'])

        #     doc = {
        #         'app_name': app_data.app_name,
        #         'app_version': app_data.app_version,
        #         'app_downloads': app_data.downloads,
        #         'release_date': app_data.release_date,
        #         'description': app_data.description,
        #     }

        #     # Create a JSON representation of the resource
        #     resp.text = json.dumps(doc, ensure_ascii=False)
        #     resp.status = falcon.HTTP_200
        # except:
        #     resp.status = falcon.HTTP_400
        

        query_params = dict(req.params.items())
        app_data = scraper.AptoideApp(query_params['url'])

        doc = {
            'app_name': app_data.app_name,
            'app_version': app_data.app_version,
            'app_downloads': app_data.downloads,
            'release_date': app_data.release_date,
            'description': app_data.description,
        }

        # Create a JSON representation of the resource
        resp.text = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
        # The following line can be omitted because 200 is the default
        # status returned by the framework, but it is included here to
        # illustrate how this may be overridden as needed.
        # resp.status = falcon.HTTP_200