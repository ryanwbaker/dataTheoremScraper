import json
import falcon # type: ignore
from . import scraper


class Resource:

    def on_get(self, req, resp):
        # Parse query string
        try:
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
        except Exception as err:
            resp.text=falcon.HTTP_405+": "+str(err)
            resp.status = falcon.HTTP_405