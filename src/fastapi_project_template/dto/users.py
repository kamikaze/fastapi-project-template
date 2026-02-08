from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict


class UserProfile(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uid: UUID
    created_at: AwareDatetime | None
    updated_at: AwareDatetime | None
    name: str | None
    email: str | None
