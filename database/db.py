# Работа с базой данных
import asyncpg
from environs import Env

ENV = Env()
ENV.read_env()


class BotDB:
    """Класс для работы с базой данных"""

    async def connection(self):
        """Подключаемся к бд"""
        return await asyncpg.connect(database=ENV('DB_NAME'), user=ENV('DB_USER'),
                                     password=ENV('DB_PASSWORD'),
                                     host=ENV('DB_HOST'), port=ENV('DB_PORT'))

    async def check_user_in_db(self, user_id: int) -> None:
        """Проверяем есть ли пользователь в базе, если нет то добавляем"""
        conn = await self.connection()
        if await conn.fetchval('SELECT tg_user_id FROM tg_bot_users WHERE tg_user_id = $1', user_id) is None:
            await conn.execute('INSERT INTO tg_bot_users (tg_user_id) VALUES ($1)', user_id)
        await conn.close()

    async def check_future_in_db(self, future: str, conn) -> int:
        """Проверяет есть ли такой фьючерс в бд, если нет добавляет его"""
        id_future = await self._give_future(future, conn)
        if id_future:
            return id_future
        else:
            await conn.execute('INSERT INTO futures (future) VALUES ($1)', future)
            return await self._give_future(future, conn)

    async def _give_future(self, future: str, conn):
        """Отдаёт id фьючерса"""
        return await conn.fetchval('SELECT * FROM futures WHERE future = $1', future)

    async def _give_user_id(self, tg_user_id: int, conn):
        """Отдаёт id пользователя"""
        return await conn.fetchval('SELECT * FROM tg_bot_users WHERE tg_user_id = $1', tg_user_id)

    async def add_future_in_list(self, tg_user_id: int, future: str) -> None:
        """Добавляет фьючерс в список отслеживаемых пользователем"""
        conn = await self.connection()
        id_user = await self._give_user_id(tg_user_id, conn)
        id_future = await self.check_future_in_db(future, conn)
        if not await conn.fetchrow(
                'SELECT users_id, futures_id FROM tg_bot_users_futures WHERE users_id = $1 and futures_id = $2',
                id_user, id_future):
            await conn.execute('INSERT INTO tg_bot_users_futures (users_id, futures_id) VALUES ($1, $2)',
                               id_user, id_future)
        await conn.close()

    async def show_my_list_futures(self, tg_user_id: int) -> list | bool:
        """Отдаёт список фьючерсов отслеживаемых пользователем"""
        conn = await self.connection()
        user_id = await self._give_user_id(tg_user_id, conn)
        futures = await conn.fetch('SELECT futures_id FROM tg_bot_users_futures WHERE users_id = $1', user_id)
        if futures:
            futures_id = []
            for f_id in futures:
                futures_id.append(f_id['futures_id'])
            fts = await conn.fetch('SELECT future FROM futures WHERE id = ANY($1) ', futures_id)
            await conn.close()
            return [ft['future'] for ft in fts]
        else:
            await conn.close()
            return False

    async def delete_future_in_my_list(self, tg_user_id: int, future: str) -> None:
        """Удаляет фьючерс из списка отслеживаемых"""
        conn = await self.connection()
        user_id = await self._give_user_id(tg_user_id, conn)
        await conn.execute('DELETE FROM tg_bot_users_futures '
                           'WHERE users_id = $1 and futures_id in (SELECT id FROM futures WHERE future = $2)',
                           user_id, future)
        await conn.close()
