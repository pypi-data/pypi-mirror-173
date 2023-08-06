import click
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.authentication_api import AuthenticationApi
from datadog_api_client.exceptions import ForbiddenException

from .load_configuration import get_datadog_configuration


def validate_api_key():
    datadog_configuration = get_datadog_configuration()
    configuration = Configuration(
        api_key=dict(apiKeyAuth=datadog_configuration["api_key"]),
        server_variables=dict(site=datadog_configuration["site"]),
    )
    with ApiClient(configuration) as api_client:
        api_instance = AuthenticationApi(api_client)
        try:
            response = api_instance.validate()
        except ForbiddenException:
            return False
        except Exception:
            return None
    return response.valid


@click.command()
def validate_api_key_cli():
    result = validate_api_key()
    if result is None:
        print("Error occurred. Please try again later.")
    elif result:
        print("api_key is OK")
    else:
        print("api_key not valid")
