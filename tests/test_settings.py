import pytest

from trace_agent.settings import ZetarisSettings


def test_loads_zetaris_settings(monkeypatch):
    monkeypatch.setenv("ZETARIS_REST_URL", "https://zetaris.example.com/api/v1.0/")
    monkeypatch.setenv("ZETARIS_ORG_ID", "42")
    monkeypatch.setenv("ZETARIS_API_KEY", "test-secret")

    settings = ZetarisSettings.from_env()

    assert settings.rest_url == "https://zetaris.example.com/api/v1.0"
    assert settings.org_id == 42
    assert settings.api_key == "test-secret"
    assert "test-secret" not in repr(settings)


def test_rejects_missing_settings(monkeypatch):
    monkeypatch.delenv("ZETARIS_REST_URL", raising=False)
    monkeypatch.delenv("ZETARIS_ORG_ID", raising=False)
    monkeypatch.delenv("ZETARIS_API_KEY", raising=False)

    with pytest.raises(ValueError, match="ZETARIS_REST_URL"):
        ZetarisSettings.from_env()


def test_rejects_invalid_url(monkeypatch):
    monkeypatch.setenv("ZETARIS_REST_URL", "not-a-url")
    monkeypatch.setenv("ZETARIS_ORG_ID", "42")
    monkeypatch.setenv("ZETARIS_API_KEY", "test-secret")

    with pytest.raises(ValueError, match="HTTP or HTTPS"):
        ZetarisSettings.from_env()


def test_requires_api_version_in_url(monkeypatch):
    monkeypatch.setenv("ZETARIS_REST_URL", "https://zetaris.example.com")
    monkeypatch.setenv("ZETARIS_ORG_ID", "42")
    monkeypatch.setenv("ZETARIS_API_KEY", "test-secret")

    with pytest.raises(ValueError, match="/api/v1.0"):
        ZetarisSettings.from_env()


def test_rejects_non_numeric_org_id(monkeypatch):
    monkeypatch.setenv(
        "ZETARIS_REST_URL",
        "https://zetaris.example.com/api/v1.0",
    )
    monkeypatch.setenv("ZETARIS_ORG_ID", "my-organisation")
    monkeypatch.setenv("ZETARIS_API_KEY", "test-secret")

    with pytest.raises(ValueError, match="numeric"):
        ZetarisSettings.from_env()