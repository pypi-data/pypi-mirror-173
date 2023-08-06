from httpx import AsyncClient, Response

from deskzor.core.tokens import inject_tokens, ZohoApi
from deskzor.core.verify import verify_data
from deskzor.models.metadata.fields import Fields, FieldsRequest


@verify_data(input_model=FieldsRequest, output_model=Fields)
@inject_tokens()
async def get_fields(client: AsyncClient, api: ZohoApi, params: dict) -> Response:
    url = f"{api.domain}/crm/{api.version}/settings/fields"
    response = await client.get(url, params=params)
    return response
