from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    # UI
    base_url: str = "https://the-internet.herokuapp.com"
    headless: bool = True
    slow_mo: int = 0
    viewport_width: int = 1920
    viewport_height: int = 1080
    timeout: int = 30_000  # ms

    # API
    api_base_url: str = "https://jsonplaceholder.typicode.com" 
    api_timeout: float = 30.0

    # Credentials (для herokuapp)
    valid_username: str = "tomsmith"
    valid_password: str = "SuperSecretPassword!"

    # Paths
    project_root: Path = Path(__file__).resolve().parent.parent
    logs_dir: Path = project_root / "logs"
    reports_dir: Path = project_root / "reports"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
settings.logs_dir.mkdir(parents=True, exist_ok=True)
settings.reports_dir.mkdir(parents=True, exist_ok=True)
