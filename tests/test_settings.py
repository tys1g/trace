import pytest

from trace_agent.settings import ZetarisSettings


def test_loads_zetaris_settings(monkeypatch):
    monkeypatch.setenv("ZETARIS_URL", "https://zetaris.example.com/")
    monkeypatch.setenv("ZETARIS_EMAIL", "user@example.com")
    monkeypatch.setenv("ZETARIS_PASSWORD", "test-secret")

    settings = ZetarisSettings.from_env()

    assert settings.url == "https://zetaris.example.com"
    assert settings.email == "user@example.com"
    assert settings.password == "test-secret"
    assert "test-secret" not in repr(settings)


def test_rejects_missing_settings(monkeypatch):
    monkeypatch.delenv("ZETARIS_URL", raising=False)
    monkeypatch.delenv("ZETARIS_EMAIL", raising=False)
    monkeypatch.delenv("ZETARIS_PASSWORD", raising=False)

    with pytest.raises(ValueError, match="ZETARIS_URL"):
        ZetarisSettings.from_env()


def test_rejects_invalid_url(monkeypatch):
    monkeypatch.setenv("ZETARIS_URL", "not-a-url")
    monkeypatch.setenv("ZETARIS_EMAIL", "user@example.com")
    monkeypatch.setenv("ZETARIS_PASSWORD", "test-secret")

    with pytest.raises(ValueError, match="HTTP or HTTPS"):
        ZetarisSettings.from_env()