from dataclasses import dataclass, field
from os import environ
from urllib.parse import urlparse


@dataclass(frozen=True)
class ZetarisSettings:
    rest_url: str
    org_id: int
    api_key: str = field(repr=False)

    @classmethod
    def from_env(cls) -> "ZetarisSettings":
        rest_url = environ.get("ZETARIS_REST_URL", "").strip().rstrip("/")
        org_id_text = environ.get("ZETARIS_ORG_ID", "").strip()
        api_key = environ.get("ZETARIS_API_KEY", "")

        missing = [
            name
            for name, value in (
                ("ZETARIS_REST_URL", rest_url),
                ("ZETARIS_ORG_ID", org_id_text),
                ("ZETARIS_API_KEY", api_key.strip()),
            )
            if not value
        ]

        if missing:
            raise ValueError(
                "Missing required environment variables: "
                + ", ".join(missing)
            )

        parsed_url = urlparse(rest_url)

        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("ZETARIS_REST_URL must be a valid HTTP or HTTPS URL")

        if parsed_url.path.rstrip("/") != "/api/v1.0":
            raise ValueError("ZETARIS_REST_URL must end in /api/v1.0")

        try:
            org_id = int(org_id_text)
        except ValueError as error:
            raise ValueError("ZETARIS_ORG_ID must be numeric") from error

        return cls(
            rest_url=rest_url,
            org_id=org_id,
            api_key=api_key,
        )