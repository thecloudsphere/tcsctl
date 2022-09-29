# based on
# - https://www.pretzellogix.net/2021/12/08/how-to-write-a-python3-sdk-library-module-for-a-json-rest-api/
# - https://github.com/PretzelLogix/py-cat-api

from urllib.parse import urljoin
import uuid as uuid_pkg

import requests
from typing import Dict

from . import logger, settings
from .exceptions import TimonApiException
from .models import *


class Client:
    def __init__(self, profile: str = 'default'):
        self.profile = settings.profiles.get(profile)
        self.api_url = urljoin(self.profile.api_url, f"{self.profile.api_version}/")

        logger.debug(f"profile = {profile}")
        logger.debug(f"api_url = {self.api_url}")

        if not self.profile.insecure:
            requests.packages.urllib3.disable_warnings()

    def _do(self, http_method: str, endpoint: str, ep_params: Dict = None, data: Dict = None, headers: Dict = {}) -> Result:
        url = urljoin(str(self.api_url), endpoint)

        log_line_pre = f"method={http_method}, url={url}, params={ep_params}, headers={headers}"
        log_line_post = ', '.join((log_line_pre, "success={}, status_code={}, message={}"))

        # Log HTTP params and perform an HTTP request, catching and re-raising any exceptions
        try:
            logger.debug(log_line_pre)
            response = requests.request(method=http_method, url=url, verify=self.profile.insecure,
                                        headers=headers, params=ep_params, json=data)
        except requests.exceptions.RequestException as e:
            logger.error(str(e))
            raise TimonApiException("Request failed") from e

        # If status_code in 200-299 range, return success Result with data, otherwise raise exception
        is_success = 299 >= response.status_code >= 200     # 200 to 299 is OK
        log_line = log_line_post.format(is_success, response.status_code, response.reason, response.headers)
        if is_success:
            logger.debug(log_line)
            return Result(status_code=response.status_code, headers=response.headers, message=response.reason, data=response.content)
        logger.error(log_line)
        raise TimonApiException(f"{response.status_code}: {response.reason}")

    def get(self, endpoint: str, ep_params: Dict = None) -> Result:
        return self._do(http_method='GET', endpoint=endpoint, ep_params=ep_params)

    def post(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method='POST', endpoint=endpoint, ep_params=ep_params, data=data)

    def delete(self, endpoint: str, ep_params: Dict = None, data: Dict = None) -> Result:
        return self._do(http_method='DELETE', endpoint=endpoint, ep_params=ep_params, data=data)

    def fetch_data(self, url: str) -> bytes:
        # GET URL; catching, logging, and re-raising any exceptions
        http_method = 'GET'
        try:
            log_line = f"method={http_method}, url={url}"
            logger.debug(log_line)
            response = requests.request(method=http_method, url=url, verify=self.profile.insecure)
        except requests.exceptions.RequestException as e:
            logger.error(str(e))
            raise TimonApiException(str(e)) from e

        # If status_code in 200-299 range, return byte stream, otherwise raise exception
        is_success = 299 >= response.status_code >= 200
        log_line = f"success={is_success}, status_code={response.status_code}, message={response.reason}"
        logger.debug(log_line)
        if not is_success:
            raise TimonApiException(response.reason)

        return response.content


class Timon:
    def __init__(self, profile: str = 'default'):
        self.profile = settings.profiles.get(profile)
        self.client = Client(profile=profile)

    # blueprints

    def delete_blueprint(self, blueprint_id: uuid_pkg.UUID, project_id: uuid_pkg.UUID) -> Result:
        result = self.client.delete(f"blueprints/{project_id}/{blueprint_id}")
        return result

    def get_blueprint(self, blueprint_id: uuid_pkg.UUID, project_id: uuid_pkg.UUID) -> Blueprint:
        result = self.client.get(f"blueprints/{project_id}/{blueprint_id}")
        blueprint = Blueprint(**result.data)
        return blueprint

    def get_blueprints(self, project_id: uuid_pkg.UUID) -> Blueprint:
        result = self.client.get(f"blueprints/{project_id}")
        blueprints = [Blueprint(**blueprint) for blueprint in result.data]
        return blueprints

    def import_blueprint(self, name: str, repository: str, repository_server: str, project_id: uuid_pkg.UUID) -> uuid_pkg.UUID:
        blueprint = BlueprintBase(
            repository=repository,
            repository_server=repository_server,
            name=name
        )
        result = self.client.post(f"blueprints/{project_id}", data=blueprint.dict())
        blueprint = Blueprint(**result.data)
        return blueprint

    # environments

    def delete_environment(self, environment_id: uuid_pkg.UUID, project_id: uuid_pkg.UUID) -> Result:
        result = self.client.delete(f"environments/{project_id}/{environment_id}")
        return result

    def get_environment(self, environment_id: uuid_pkg.UUID, project_id: uuid_pkg.UUID) -> Environment:
        result = self.client.get(f"environments/{project_id}/{environment_id}")
        environment = Environment(**result.data)
        return environment

    def get_environments(self, project_id: uuid_pkg.UUID) -> Environment:
        result = self.client.get(f"environments/{project_id}")
        environments = [Environment(**environment) for environment in result.data]
        return environments

    def import_environment(self, name: str, repository: str, repository_server: str, project_id: uuid_pkg.UUID) -> uuid_pkg.UUID:
        environment = EnvironmentBase(
            repository=repository,
            repository_server=repository_server,
            name=name
        )
        result = self.client.post(f"environments/{project_id}", data=environment.dict())
        environment = Environment(**result.data)
        return environment

    # other

    def login(self) -> None:
        pass

    def logout(self) -> None:
        pass
