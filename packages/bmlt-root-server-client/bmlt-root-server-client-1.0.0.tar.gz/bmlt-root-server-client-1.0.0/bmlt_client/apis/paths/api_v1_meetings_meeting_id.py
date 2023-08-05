from bmlt_client.paths.api_v1_meetings_meeting_id.get import ApiForget
from bmlt_client.paths.api_v1_meetings_meeting_id.put import ApiForput
from bmlt_client.paths.api_v1_meetings_meeting_id.delete import ApiFordelete
from bmlt_client.paths.api_v1_meetings_meeting_id.patch import ApiForpatch


class ApiV1MeetingsMeetingId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
