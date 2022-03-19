from origin.models.auth import InternalToken
from fastapi import Depends, HTTPException
from src.meteringpoints_api.fake_data import token_encoder


async def internal_token_provider(
        token: str,
        # token_encoder: TokenEncoder[InternalToken] = Depends(TokenEncoder),
) -> InternalToken:
    """Decompose token into an OpaqueToken."""

    try:
        internal_token = token_encoder.decode(token)

    except token_encoder.DecodeError:
        raise HTTPException(status_code=500)

    if not internal_token.is_valid:
        raise HTTPException(status_code=403, detail="invalid token")

    return internal_token


class RequiresScope:
    """Only Allows requests with specific scopes granted."""

    def __init__(self, scope: str):
        self.scope = scope

    def __call__(self,
                 token: InternalToken = Depends(internal_token_provider)):
        if self.scope not in token.scope:
            return False


class RequiresActor:
    """Only Allows requests with specific scopes granted."""

    def __init__(self, actor: str):
        self.actor = actor

    def __call__(self,
                 token: InternalToken = Depends(internal_token_provider)):
        if self.actor not in token.actor:
            raise HTTPException(status_code=404, detail="Actor not found")
