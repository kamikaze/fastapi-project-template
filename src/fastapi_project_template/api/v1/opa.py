import logging
from typing import Annotated

import aiohttp
from fastapi import Depends, HTTPException, Request
from python3_commons.auth import TokenData
from starlette import status

from fastapi_project_template.api.v1.auth import get_verified_token
from fastapi_project_template.conf import settings

logger = logging.getLogger(__name__)


async def check_opa_authorization(request: Request, token_data: TokenData) -> bool:
    if (opa_url := settings.opa_url) is None:
        return True

    roles = getattr(token_data, 'roles', [])

    opa_input = {
        'input': {
            'method': request.method,
            'path': request.url.path,
            'uri': str(request.url),
            'user': {'roles': roles},
        }
    }

    msg = f'{opa_input=}'
    logger.info(msg)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(str(opa_url), json=opa_input) as response:
                response.raise_for_status()
                data = await response.json()
                result = data.get('result', {})

                allowed = result.get('allow', False)

                msg = (
                    f'OPA authorization request: method={request.method}, path={request.url.path}, '
                    f'roles={roles}, allowed={allowed}, result={result}'
                )
                logger.info(msg)

                if not allowed:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN, detail='Access denied by policy service.'
                    )

                return True
        except aiohttp.ClientError as e:
            logger.exception('Error communicating with policy service.')

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Error validating authorization'
            ) from e


async def opa_authorize(
    request: Request,
    token: Annotated[TokenData, Depends(get_verified_token)],
) -> None:
    await check_opa_authorization(request, token)
