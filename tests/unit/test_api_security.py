from datetime import UTC, datetime, timedelta

from foreightkillo.security import ApiKeyAuthenticator, Principal, SignedWebhook


def test_api_keys_are_scoped_and_not_stored_in_plaintext() -> None:
    auth = ApiKeyAuthenticator()
    principal = Principal("operator", "operator", frozenset({"market:read"}))
    auth.register("key", "a-secure-development-key-123", principal, b"fixed-test-salt")
    assert auth.authenticate("key.a-secure-development-key-123", "market:read") == principal
    assert auth.authenticate("key.a-secure-development-key-123", "orders:write") is None
    assert auth.authenticate("key.wrong-secret-that-is-long-enough", "market:read") is None


def test_webhook_signature_and_replay_window() -> None:
    now = datetime(2026, 8, 8, tzinfo=UTC)
    webhook = SignedWebhook.create(b'{"event":"health"}', "webhook-secret", now)
    assert webhook.verify("webhook-secret", now)
    assert not webhook.verify("wrong", now)
    assert not webhook.verify("webhook-secret", now + timedelta(minutes=6))
