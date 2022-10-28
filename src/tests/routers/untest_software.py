"""
src.tests.routers.untest_software - NOT FULLY IMPLEMENTED
"""

from src.tests.utils.db import demo_api
from generated.schema import Software



def test_software_crd():
    """
    Test creation, retrieval and delete operations for software.

    Note: There currently isn't a way to modify sofware so an
          update has not been implemented
    """
    with demo_api('software') as client:
        software = Software(source='test', storage_uri='http://')
        response_post = client.post(
            '/software',
            data=software.json(),
            headers={'Content-type': 'application/json', 'Accept': 'text/plain'}
        )
        assert 200 == response_post.status_code
        id = response_post.json()
        response_get = client.get(f'/software/${id}')
        assert 200 == response_get.status_code
        result = Software.parse_obj(response_get.json())
        assert software == result
