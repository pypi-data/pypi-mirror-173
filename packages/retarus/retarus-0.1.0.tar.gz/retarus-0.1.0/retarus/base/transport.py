from email import message
from typing import List
from aiohttp_retry import RetryClient, ExponentialRetry
from aiohttp import ClientResponse
import logging

from retarus.base.config import Configuration
from retarus.base import exceptions
from retarus.base.region import RegionUri, region_resolve


class Transporter:
    retry_options = ExponentialRetry(attempts=1)

    def __init__(self, uris):
        self.service_uri_regions = uris

    async def post(self, path: str, payload: dict):
        self.__validate_auth()
        region = region_resolve(Configuration.region, self.service_uri_regions)
        url = f"{region.ha_uri}/rest/v1/{path}"
        async with RetryClient(retry_options=self.retry_options) as session:
            async with session.post(
                url=url, json=payload, headers=Configuration.auth
            ) as resp:
                return await self.__match_response(resp)

    async def get(self, path: str, query_parms: dict = {}):
        self.__validate_auth()
        async with RetryClient(retry_options=self.retry_options) as session:

            @fetch_datacenter(regions=self.service_uri_regions)
            async def get(host: str):
                url = f"{host}/rest/v1/{path}"
                async with session.get(
                    url=url, headers=Configuration.auth, params=query_parms
                ) as resp:
                    return await self.__match_response(resp)

            return await get()

    async def delete(self, path: str):
        self.__validate_auth()

        async with RetryClient(retry_options=self.retry_options) as session:

            @fetch_datacenter(regions=self.service_uri_regions)
            async def delete(host: str):
                url = f"{host}/rest/v1/{path}"

                async with session.delete(url=url, headers=Configuration.auth) as resp:
                    return await self.__match_response(resp)

        return await delete()

    async def __match_response(self, resp: ClientResponse):
        logging.debug(resp.status)
        if resp.status == 401:
            raise exceptions.ApiAuthorizationError()
        elif resp.status == 400:
            raise exceptions.ApiInvalidPayload()
        elif resp.status == 404:
            return False
        elif resp.status == 200 or resp.status == 201:
            data = await resp.json()
            return data
        raise exceptions.SDKError(
            message="An unexpected error occurred, there migth be something wrong with the sdk.\n"
            "Please contact the Retarus support"
        )

    @staticmethod
    def __validate_auth():
        """
        Validates the global sdk configuration, if the required value are not set it will raise a ConfigurationError
        """
        if Configuration.auth == {}:
            raise exceptions.ConfigurationError(
                message="You need to configure the SDK using the static Configuration class"
            )


def fetch_datacenter(regions: List[RegionUri]):
    """
    A decorator to iterate over a list of hostnames a check for a valid response.
    """
    uri = region_resolve(Configuration.region, regions)

    def wrap(func):
        def wrapped(*args):
            for server in uri.urls:
                print(server)
                print("123")
                res = func(server)
                if res is False:
                    continue
                return res
            raise exceptions.SDKError(message="No report found, there must be an issue with the sdk.")
        return wrapped

    return wrap
