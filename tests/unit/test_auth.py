import msgspec

from fastapi_project_template.api.v1.auth import AppTokenData

BASE_CLAIMS = {'exp': 2, 'iat': 1, 'iss': 'http://localhost:5556/dex', 'sub': 'user', 'aud': 'frontend'}


def test_roles_from_groups_claim() -> None:
    token = msgspec.convert({**BASE_CLAIMS, 'groups': ['admin', 'view-profile']}, type=AppTokenData)

    assert sorted(token.roles) == ['admin', 'view-profile']


def test_roles_merge_keycloak_claims_and_groups() -> None:
    claims = {
        **BASE_CLAIMS,
        'realm_access': {'roles': ['view-profile']},
        'resource_access': {'frontend': {'roles': ['admin']}},
        'groups': ['admin', 'ops'],
    }
    token = msgspec.convert(claims, type=AppTokenData)

    assert sorted(token.roles) == ['admin', 'ops', 'view-profile']


def test_roles_empty_without_role_claims() -> None:
    token = msgspec.convert(BASE_CLAIMS, type=AppTokenData)

    assert token.roles == []
