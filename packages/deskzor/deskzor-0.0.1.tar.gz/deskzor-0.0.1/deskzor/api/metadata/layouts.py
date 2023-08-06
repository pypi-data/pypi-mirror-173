from httpx import AsyncClient, Response

from deskzor.core.tokens import inject_tokens, ZohoApi
from deskzor.core.verify import verify_data
from deskzor.models.metadata.layouts import Layouts, LayoutsRequest


@verify_data(input_model=LayoutsRequest, output_model=Layouts)
@inject_tokens()
async def get_layouts(client: AsyncClient, api: ZohoApi, params: dict) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/layouts"
    response = await client.get(url, params=params)
    return response
