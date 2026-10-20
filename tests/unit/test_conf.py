import pytest

from fastapi_project_template.conf import Settings


def test_allowed_origins_default() -> None:
    assert Settings().allowed_origins == ('*',)


def test_allowed_origins_from_comma_separated_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv('ALLOWED_ORIGINS', 'http://a.example, http://b.example')

    assert Settings().allowed_origins == ('http://a.example', 'http://b.example')
