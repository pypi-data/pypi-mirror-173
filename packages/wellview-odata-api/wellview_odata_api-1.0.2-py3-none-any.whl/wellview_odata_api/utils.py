import wellview_odata_api
from typing import Text

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def get_api_client(host:Text, api_token:Text, verify_ssl:bool = False) -> wellview_odata_api.ApiClient:
        # Configure API key authorization: bearerAuth
        configuration = wellview_odata_api.Configuration()
        configuration.api_key['Authorization'] = api_token
        # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
        configuration.api_key_prefix['Authorization'] = 'Bearer'
        configuration.verify_ssl = verify_ssl
        configuration.host = host

        return wellview_odata_api.ApiClient(configuration)
