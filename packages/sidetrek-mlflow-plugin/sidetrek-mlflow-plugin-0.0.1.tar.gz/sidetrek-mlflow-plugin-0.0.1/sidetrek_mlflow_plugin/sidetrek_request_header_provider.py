from mlflow.tracking.request_header.abstract_request_header_provider import RequestHeaderProvider
from mlflow.utils import env
import os

class SideTrekRequestHeaderProvider(RequestHeaderProvider):
    """
    Provides request headers indicating the type of Databricks environment from which a request
    was made.
    """

    def in_context(self):
        return True

    def request_headers(self):
        request_headers = {}
        
        request_headers["project_id"] = os.getenv('SIDETREK_PROJECT_ID')
        request_headers["user_id"] = os.getenv('SIDETREK_USER_ID')
        request_headers["organization_id"] = os.getenv('SIDETREK_ORGANIZATION_ID')

        return request_headers