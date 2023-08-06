from base64 import urlsafe_b64encode

from retarus.base.region import Region


class Configuration(object):
    url: str = "https://faxws.de1.retarus.com/rest/v1"
    region: Region = Region.Europe
    auth: dict = {}
    customer_number: str = ""

    @staticmethod
    def set_auth(user_id: str, password: str):
        auth_string = f"{user_id}:{password}"
        auth_string = urlsafe_b64encode(auth_string.encode('UTF-8')).decode('ascii')

        Configuration.auth = {"Authorization": f"Basic {auth_string}", "Content-Type": "application/json"}

    @staticmethod
    def set_region(region: Region):
        Configuration.region = region
