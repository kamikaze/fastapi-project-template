import os
import subprocess
import sys
from http import HTTPStatus
from unittest.mock import AsyncMock

import httpx
import pytest
from fastapi_commons.exceptions import UnauthorizedError

from fastapi_project_template.api.http import app
from fastapi_project_template.api.v1.auth import get_current_token
from fastapi_project_template.conf import oidc_settings
from fastapi_project_template.db import async_session_manager

BASE_URL = 'http://test'


@pytest.fixture(autouse=True)
def _oidc_authority(monkeypatch: pytest.MonkeyPatch) -> None:
    # The OIDC client is created lazily, so an unreachable authority is fine for requests that never verify a token.
    monkeypatch.setattr(oidc_settings, 'authority_url', 'http://oidc.invalid/realm')


@pytest.mark.asyncio
async def test_alive_with_lifespan() -> None:
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL) as client,
    ):
        response = await client.get('/api/app/v1/alive')

    assert response.status_code == HTTPStatus.OK
    assert response.json() is True


@pytest.mark.asyncio
async def test_protected_endpoint_requires_credentials() -> None:
    async with (
        app.router.lifespan_context(app),
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=BASE_URL) as client,
    ):
        response = await client.get('/api/app/v1/users/me')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.asyncio
async def test_current_token_rejects_missing_identity() -> None:
    with pytest.raises(UnauthorizedError):
        await get_current_token(None)


@pytest.mark.asyncio
async def test_lifespan_disposes_database_engines(monkeypatch: pytest.MonkeyPatch) -> None:
    aclose = AsyncMock()
    monkeypatch.setattr(async_session_manager, 'aclose', aclose)

    async with app.router.lifespan_context(app):
        aclose.assert_not_awaited()

    aclose.assert_awaited_once()


def test_verified_token_is_none_when_auth_disabled() -> None:
    code = (
        'import asyncio\n'
        'from fastapi_project_template.api.v1.auth import get_verified_token\n'
        'assert asyncio.run(get_verified_token()) is None\n'
    )

    assert _run_with_auth_disabled(code).returncode == 0


def test_protected_endpoint_answers_401_when_auth_disabled() -> None:
    code = (
        'import asyncio, httpx\n'
        'from fastapi_project_template.api.http import app\n'
        'async def main():\n'
        '    async with app.router.lifespan_context(app):\n'
        '        transport = httpx.ASGITransport(app=app)\n'
        '        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:\n'
        '            print("STATUS", (await client.get("/api/app/v1/users/me")).status_code)\n'
        'asyncio.run(main())\n'
    )

    result = _run_with_auth_disabled(code)

    assert result.returncode == 0, result.stderr
    # The app logs to stdout too, so the status is read from a tagged line.
    statuses = [line.split()[-1] for line in result.stdout.splitlines() if line.startswith('STATUS ')]

    assert statuses == [str(HTTPStatus.UNAUTHORIZED.value)]


def _run_with_auth_disabled(code: str) -> subprocess.CompletedProcess[str]:
    env = {**os.environ, 'API_AUTH_ENABLED': 'false'}

    return subprocess.run(  # noqa: S603
        [sys.executable, '-c', code], env=env, capture_output=True, text=True, check=False
    )
