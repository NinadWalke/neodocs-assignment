import os

def get_env(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


DATABASE_PATH = get_env("DATABASE_PATH")
SERVER_HOST = get_env("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(get_env("SERVER_PORT", "8000"))
