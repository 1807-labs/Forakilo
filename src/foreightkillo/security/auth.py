"""Installation-local API keys stored only as scrypt digests."""

from __future__ import annotations

import hmac
from dataclasses import dataclass
from hashlib import scrypt
from secrets import token_bytes


@dataclass(frozen=True, slots=True)
class Principal:
    principal_id: str
    role: str
    scopes: frozenset[str]


@dataclass(frozen=True, slots=True)
class _Credential:
    salt: bytes
    digest: bytes
    principal: Principal


class ApiKeyAuthenticator:
    def __init__(self) -> None:
        self._credentials: dict[str, _Credential] = {}

    def register(
        self, key_id: str, secret: str, principal: Principal, salt: bytes | None = None
    ) -> None:
        if len(secret) < 24:
            raise ValueError("API key secret must contain at least 24 characters")
        actual_salt = salt or token_bytes(16)
        self._credentials[key_id] = _Credential(
            actual_salt, self._derive(secret, actual_salt), principal
        )

    def authenticate(self, presented: str, required_scope: str) -> Principal | None:
        key_id, separator, secret = presented.partition(".")
        if not separator or not key_id or not secret:
            return None
        credential = self._credentials.get(key_id)
        if credential is None:
            return None
        candidate = self._derive(secret, credential.salt)
        if not hmac.compare_digest(candidate, credential.digest):
            return None
        if required_scope not in credential.principal.scopes:
            return None
        return credential.principal

    @staticmethod
    def _derive(secret: str, salt: bytes) -> bytes:
        return scrypt(secret.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)
