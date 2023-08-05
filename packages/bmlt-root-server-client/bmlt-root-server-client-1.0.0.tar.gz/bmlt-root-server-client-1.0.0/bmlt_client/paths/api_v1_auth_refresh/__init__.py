# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from bmlt_client.paths.api_v1_auth_refresh import Api

from bmlt_client.paths import PathValues

path = PathValues.API_V1_AUTH_REFRESH