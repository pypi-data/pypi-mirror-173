from bmlt_client.paths.api_v1_formats_format_id.get import ApiForget
from bmlt_client.paths.api_v1_formats_format_id.put import ApiForput
from bmlt_client.paths.api_v1_formats_format_id.delete import ApiFordelete
from bmlt_client.paths.api_v1_formats_format_id.patch import ApiForpatch


class ApiV1FormatsFormatId(
    ApiForget,
    ApiForput,
    ApiFordelete,
    ApiForpatch,
):
    pass
