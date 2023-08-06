import logging
from typing_extensions import dataclass_transform

from .exceptions import AuthorizationError, DependencyTrackApiError

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Bom:
    """Class dedicated to all "folders" related endpoints"""

    def list_project_bom(self, uuid):
        """List all components accessible to the authenticated user

        API Endpoint: GET /bom/cyclonedx/project/{uuid}

        :return: a list of bom in project
        :rtype: list()
        :raises DependencyTrackApiError: if the REST call failed
        """
        response = self.session.get(self.api + f"/bom/cyclonedx/project/{uuid}", params=self.paginated_param_payload)
        if response.status_code == 200:
            return response.json()
        else:
            description = f"Unable to get a list of components"
            raise DependencyTrackApiError(description, response)

    def upload_project_bom(self, uuid, file):
        """Get details of project dependency.
    
        API Endpoint: POST /bom
    
        :param id: the ID of the project to be analysed
        :type id: int
        :return: the requested project dependency
        :rtype: dist
        :raises DependencyTrackApiError: if the REST call failed
        """
        files = open(file, "rb")
        data = {"project": uuid}

        response = self.session.post(self.api + f"/bom", files={"bom": files}, data=data)

        if response.status_code == 200:
            return response.json()
        else:
            description = f"Error while getting dependency for component {uuid}"
            raise DependencyTrackApiError(description, response)



