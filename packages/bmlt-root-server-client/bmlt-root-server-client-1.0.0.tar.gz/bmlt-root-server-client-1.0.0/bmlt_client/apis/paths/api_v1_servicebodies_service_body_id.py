from bmlt_client.paths.api_v1_servicebodies_service_body_id.get import ApiForget
from bmlt_client.paths.api_v1_servicebodies_service_body_id.put import ApiForput
from bmlt_client.paths.api_v1_servicebodies_service_body_id.delete import ApiFordelete
from bmlt_client.paths.api_v1_servicebodies_service_body_id.patch import ApiForpatch


class ApiV1ServicebodiesServiceBodyId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
