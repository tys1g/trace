from collections.abc import Callable
from dataclasses import dataclass, field
from json import dumps, loads
from os import environ
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

TextGenerator = Callable[[str, str | None], str]


@dataclass(frozen=True)
class GeneratorSettings:
    base_url: str
    model: str
    api_key: str = field(repr=False)

    @classmethod
    def from_env(cls) -> "GeneratorSettings":
        base_url = environ.get("GENERATOR_BASE_URL", "").strip().rstrip("/")
        model = environ.get("GENERATOR_MODEL", "").strip()
        api_key = environ.get("GENERATOR_API_KEY", "").strip()

        missing = [
            name
            for name, value in (
                ("GENERATOR_BASE_URL", base_url),
                ("GENERATOR_MODEL", model),
                ("GENERATOR_API_KEY", api_key),
            )
            if not value
        ]

        if missing:
            raise ValueError(
                "Missing required environment variables: " + ", ".join(missing)
            )

        parsed_url = urlparse(base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise ValueError("GENERATOR_BASE_URL must be a valid HTTP or HTTPS URL")

        return cls(base_url=base_url, model=model, api_key=api_key)


def create_generator(
    settings: GeneratorSettings | None = None,
    *,
    timeout: float = 60.0,
) -> TextGenerator:
    """Create a reusable text generator backed by an OpenAI-compatible API."""
    config = settings or GeneratorSettings.from_env()

    def generate(prompt: str, system_prompt: str | None = None) -> str:
        if not prompt.strip():
            raise ValueError("prompt must be a non-empty string")

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = dumps(
            {
                "model": config.model,
                "messages": messages,
                "temperature": 0.2,
                "max_tokens": 512,
                "stream": False,
            }
        ).encode("utf-8")

        request = Request(
            url=f"{config.base_url}/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=timeout) as response:
                result = loads(response.read().decode("utf-8"))
        except HTTPError as error:
            raise RuntimeError(
                f"Model provider returned HTTP {error.code}"
            ) from error
        except URLError as error:
            raise RuntimeError(
                "Could not reach the configured model provider"
            ) from error

        try:
            text = result["choices"][0]["message"]["content"]
        except (IndexError, KeyError, TypeError) as error:
            raise ValueError(
                "Model provider returned an unexpected response"
            ) from error

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Model provider returned an empty response")

        return text.strip()

    return generate