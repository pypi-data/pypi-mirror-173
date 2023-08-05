from bmlt_client.paths.api_v1_users_user_id.get import ApiForget
from bmlt_client.paths.api_v1_users_user_id.put import ApiForput
from bmlt_client.paths.api_v1_users_user_id.delete import ApiFordelete
from bmlt_client.paths.api_v1_users_user_id.patch import ApiForpatch


class ApiV1UsersUserId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
