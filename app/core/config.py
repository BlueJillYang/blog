import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator


random_secret = "RFqU71I_fSAgyPCBvNaOt_hxCZ9Qv-pEAUsnFGKA8-4"  # secrets.token_urlsafe(32)
env_api = "prod-api"  # "dev-api"


class Settings:
    provider = "mysql"
    host = "172.17.0.1"
    user = "root"
    passwd = "python123"
    POSTGRES_DB = "fastAPI"
    # SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    # SQLALCHEMY_DATABASE_URI = (
    #     f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    # )
    # （mysql数据库）
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{user}:{passwd}@{host}/{POSTGRES_DB}"
    )

    API_V1_STR = "/api"

    EMAILS_ENABLED = True
    EMAIL_TEMPLATES_DIR = "/app/templates/email-templates/build"

    EMAILS_FROM_EMAIL = "xx@qq.com"
    EMAILS_FROM_NAME = ""
    PROJECT_NAME = ""

    SMTP_TLS = True
    SMTP_PORT = 25
    SMTP_HOST = "smtp.qq.com"
    SMTP_USER = EMAILS_FROM_EMAIL
    SMTP_PASSWORD = ""

    SECRET_KEY = random_secret
    # 60 minutes * 24 hours * 8 days = 8 days
    # 60 minutes * 24 hours = 1 day
    ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 6
    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str
    SENTRY_DSN: Optional[HttpUrl] = None

    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values["PROJECT_NAME"]
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    @validator("EMAILS_ENABLED", pre=True)
    def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
        return bool(
            values.get("SMTP_HOST")
            and values.get("SMTP_PORT")
            and values.get("EMAILS_FROM_EMAIL")
        )

    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str
    USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
# now_secret = settings.SECRET_KEY
# print("settings   now Secret = ", now_secret)

