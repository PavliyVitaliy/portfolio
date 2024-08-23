import os
from enum import Enum


class MissingEnvironmentVariable(Exception):
    pass


class Env(Enum):
    PROD: str = "production"
    TEST: str = "test"
    DEV: str = "development"


def get_env_file() -> str:
    environment: str = os.getenv("ENVIRONMENT", str(Env.DEV.value))
    match environment:
        case str(Env.PROD.value):
            return ".env.prod"
        case str(Env.TEST.value):
            return ".env.test"
        case str(Env.DEV.value):
            return ".env"
        case _:
            raise MissingEnvironmentVariable(f"{environment} is not supported")
