from dataclasses import dataclass, field
from os import environ
from urllib.parse import urlparse


@dataclass(frozen=True)
class ZetarisSettings:
    url: str
    email: str
    password: str = field(repr=False)

    @classmethod
    def from_env(cls) -> "ZetarisSettings":
        url = environ.get("ZETARIS_URL", "").strip()
        email = environ.get("ZETARIS_EMAIL", "").strip()
        password = environ.get("ZETARIS_PASSWORD", "")

        missing = [
            name
            for name, value in (
                ("ZETARIS_URL", url),
                ("ZETARIS_EMAIL", email),
                ("ZETARIS_PASSWORD", password.strip()),
            )
            if not value
        ]

        if missing:
            raise ValueError(
                "Missing required environment variables: "
                + ", ".join(missing)
            )

        parsed_url = urlparse(url)

        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("ZETARIS_URL must be a valid HTTP or HTTPS URL")

        return cls(
            url=url.rstrip("/"),
            email=email,
            password=password,
        )