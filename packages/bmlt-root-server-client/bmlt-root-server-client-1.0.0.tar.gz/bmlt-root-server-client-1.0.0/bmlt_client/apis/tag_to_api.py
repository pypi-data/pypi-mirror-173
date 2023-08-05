import typing_extensions

from bmlt_client.apis.tags import TagValues
from bmlt_client.apis.tags.root_server_api import RootServerApi

TagToApi = typing_extensions.TypedDict(
    'TagToApi',
    {
        TagValues.ROOT_SERVER: RootServerApi,
    }
)

tag_to_api = TagToApi(
    {
        TagValues.ROOT_SERVER: RootServerApi,
    }
)
