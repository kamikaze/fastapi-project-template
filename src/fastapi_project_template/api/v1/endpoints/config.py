import logging

from fastapi import APIRouter
from fastapi_commons.handlers import handle_exceptions
from python3_commons.conf import oidc_settings

from fastapi_project_template.api.v1.schema import AppConfig

logger = logging.getLogger(__name__)

router = APIRouter(tags=['config'])


@router.get('/config', include_in_schema=True)
@handle_exceptions
async def get_app_config() -> AppConfig:
    return AppConfig(
        oidc_authority_url=oidc_settings.authority_url,
        oidc_client_id=oidc_settings.client_id,
        oidc_redirect_uri=oidc_settings.redirect_uri,
        oidc_scopes=oidc_settings.scopes,
    )
