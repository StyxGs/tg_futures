# Работа с базой данных

from config.config import connecting_to_db


class BotDB:
    """Класс для работы с базой данных"""

    def __init__(self):
        """Подключаемся к бд"""
        self.conn = connecting_to_db()
        self.cursor = self.conn.cursor()

    def check_user_in_db(self, user_id: int) -> None:
        """Проверяем есть ли пользователь в базе, если нет то добавляем"""
        self.cursor.execute('SELECT tg_user_id FROM tg_bot_users WHERE tg_user_id = %s', (user_id,))
        if self.cursor.fetchone() is None:
            self.cursor.execute('INSERT INTO tg_bot_users (tg_user_id) VALUES (%s)', (user_id,))
            self.conn.commit()

    def check_future_in_db(self, future: str) -> int:
        """Проверяет есть ли такой фьючерс в бд, если нет добавляет его"""
        id_future = self._give_future(future)
        if id_future:
            return id_future[0]
        else:
            self.cursor.execute('INSERT INTO futures (future) VALUES (%s)', (future,))
            self.conn.commit()
            return self._give_future(future)[0]

    def _give_future(self, future: str):
        """Отдаёт id фьючерса"""
        self.cursor.execute('SELECT * FROM futures WHERE future = (%s)', (future,))
        return self.cursor.fetchone()

    def _give_user_id(self, tg_user_id: int):
        self.cursor.execute('SELECT * FROM tg_bot_users WHERE tg_user_id = (%s)', (tg_user_id,))
        return self.cursor.fetchone()[0]

    def add_future_in_list(self, tg_user_id: int, future: str) -> None:
        """Добавляет фьючерс в список отслеживаемых пользователем"""
        id_user = self._give_user_id(tg_user_id)
        id_future = self.check_future_in_db(future)
        self.cursor.execute(
            'SELECT users_id, futures_id FROM tg_bot_users_futures WHERE users_id = (%s) and futures_id = (%s)',
            (id_user, id_future))
        if not self.cursor.fetchone():
            self.cursor.execute('INSERT INTO tg_bot_users_futures (users_id, futures_id) VALUES (%s, %s)',
                                (id_user, id_future))
            self.conn.commit()

    def show_my_list_futures(self, tg_user_id: int) -> list | bool:
        """Отдаёт список фьючерсов отслеживаемых пользователем"""
        user_id = self._give_user_id(tg_user_id)
        self.cursor.execute('SELECT futures_id FROM tg_bot_users_futures WHERE users_id = %s', (user_id,))
        futures = self.cursor.fetchall()
        if futures:
            futures_id = []
            for f_id in futures:
                futures_id.append(f_id[0])
            self.cursor.execute('SELECT future FROM futures WHERE id IN %s', [tuple(futures_id)])
            return self.cursor.fetchall()
        else:
            return False

    def delete_future_in_my_list(self, tg_user_id: int, future: str) -> None:
        """Удаляет фьючерс из списка отслеживаемых"""
        user_id = self._give_user_id(tg_user_id)
        self.cursor.execute('DELETE FROM tg_bot_users_futures '
                            'WHERE users_id = %s and futures_id in (SELECT id FROM futures WHERE future = %s)',
                            (user_id, future))
        self.conn.commit()