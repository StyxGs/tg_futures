from dataclasses import dataclass

from environs import Env

ENV = Env()
ENV.read_env()


@dataclass
class TgBot:
    token: str
    admin_id: int


@dataclass
class Config:
    tgbot: TgBot


def load_config(path: str | None = None) -> Config:
    """Функция для загрузки конфигурационных данных о боте"""
    return Config(TgBot(token=ENV('TOKEN'), admin_id=ENV('ADMIN_ID')))
