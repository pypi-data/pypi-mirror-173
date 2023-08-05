# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from bmlt_client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    API_V1_FORMATS = "/api/v1/formats"
    API_V1_FORMATS_FORMAT_ID = "/api/v1/formats/{formatId}"
    API_V1_MEETINGS = "/api/v1/meetings"
    API_V1_MEETINGS_MEETING_ID = "/api/v1/meetings/{meetingId}"
    API_V1_SERVICEBODIES = "/api/v1/servicebodies"
    API_V1_SERVICEBODIES_SERVICE_BODY_ID = "/api/v1/servicebodies/{serviceBodyId}"
    API_V1_AUTH_TOKEN = "/api/v1/auth/token"
    API_V1_AUTH_REFRESH = "/api/v1/auth/refresh"
    API_V1_AUTH_LOGOUT = "/api/v1/auth/logout"
    API_V1_USERS = "/api/v1/users"
    API_V1_USERS_USER_ID = "/api/v1/users/{userId}"
