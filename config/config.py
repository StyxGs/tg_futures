from dataclasses import dataclass

import psycopg2
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


def connecting_to_db() -> psycopg2:
    """Подключение к базе данных"""
    return psycopg2.connect(dbname=ENV('DB_NAME'), user=ENV('DB_USER'), password=ENV('DB_PASSWORD'),
                            host=ENV('DB_HOST'), port=ENV('DB_PORT'))
