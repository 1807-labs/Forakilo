"""Signed provider-neutral webhooks with replay-resistant timestamps."""

from __future__ import annotations

import hmac
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from hashlib import sha256


@dataclass(frozen=True, slots=True)
class SignedWebhook:
    timestamp: int
    signature: str
    body: bytes

    @classmethod
    def create(cls, body: bytes, secret: str, now: datetime) -> SignedWebhook:
        timestamp = int(now.astimezone(UTC).timestamp())
        payload = str(timestamp).encode() + b"." + body
        return cls(timestamp, hmac.new(secret.encode(), payload, sha256).hexdigest(), body)

    def verify(
        self, secret: str, now: datetime, tolerance: timedelta = timedelta(minutes=5)
    ) -> bool:
        observed = datetime.fromtimestamp(self.timestamp, UTC)
        if abs(now.astimezone(UTC) - observed) > tolerance:
            return False
        expected = self.create(self.body, secret, observed).signature
        return hmac.compare_digest(expected, self.signature)
