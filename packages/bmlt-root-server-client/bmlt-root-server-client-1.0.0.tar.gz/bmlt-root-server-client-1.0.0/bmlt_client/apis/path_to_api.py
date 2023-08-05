import typing_extensions

from bmlt_client.paths import PathValues
from bmlt_client.apis.paths.api_v1_formats import ApiV1Formats
from bmlt_client.apis.paths.api_v1_formats_format_id import ApiV1FormatsFormatId
from bmlt_client.apis.paths.api_v1_meetings import ApiV1Meetings
from bmlt_client.apis.paths.api_v1_meetings_meeting_id import ApiV1MeetingsMeetingId
from bmlt_client.apis.paths.api_v1_servicebodies import ApiV1Servicebodies
from bmlt_client.apis.paths.api_v1_servicebodies_service_body_id import ApiV1ServicebodiesServiceBodyId
from bmlt_client.apis.paths.api_v1_auth_token import ApiV1AuthToken
from bmlt_client.apis.paths.api_v1_auth_refresh import ApiV1AuthRefresh
from bmlt_client.apis.paths.api_v1_auth_logout import ApiV1AuthLogout
from bmlt_client.apis.paths.api_v1_users import ApiV1Users
from bmlt_client.apis.paths.api_v1_users_user_id import ApiV1UsersUserId

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.API_V1_FORMATS: ApiV1Formats,
        PathValues.API_V1_FORMATS_FORMAT_ID: ApiV1FormatsFormatId,
        PathValues.API_V1_MEETINGS: ApiV1Meetings,
        PathValues.API_V1_MEETINGS_MEETING_ID: ApiV1MeetingsMeetingId,
        PathValues.API_V1_SERVICEBODIES: ApiV1Servicebodies,
        PathValues.API_V1_SERVICEBODIES_SERVICE_BODY_ID: ApiV1ServicebodiesServiceBodyId,
        PathValues.API_V1_AUTH_TOKEN: ApiV1AuthToken,
        PathValues.API_V1_AUTH_REFRESH: ApiV1AuthRefresh,
        PathValues.API_V1_AUTH_LOGOUT: ApiV1AuthLogout,
        PathValues.API_V1_USERS: ApiV1Users,
        PathValues.API_V1_USERS_USER_ID: ApiV1UsersUserId,
    }
)

path_to_api = PathToApi(
    {
        PathValues.API_V1_FORMATS: ApiV1Formats,
        PathValues.API_V1_FORMATS_FORMAT_ID: ApiV1FormatsFormatId,
        PathValues.API_V1_MEETINGS: ApiV1Meetings,
        PathValues.API_V1_MEETINGS_MEETING_ID: ApiV1MeetingsMeetingId,
        PathValues.API_V1_SERVICEBODIES: ApiV1Servicebodies,
        PathValues.API_V1_SERVICEBODIES_SERVICE_BODY_ID: ApiV1ServicebodiesServiceBodyId,
        PathValues.API_V1_AUTH_TOKEN: ApiV1AuthToken,
        PathValues.API_V1_AUTH_REFRESH: ApiV1AuthRefresh,
        PathValues.API_V1_AUTH_LOGOUT: ApiV1AuthLogout,
        PathValues.API_V1_USERS: ApiV1Users,
        PathValues.API_V1_USERS_USER_ID: ApiV1UsersUserId,
    }
)
