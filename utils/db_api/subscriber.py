import sqlite3


class SQLighter:

    def __init__(self):
        # подключаемся к бд
        self.connection = sqlite3.connect('catbd.db')
        self.cursor = self.connection.cursor()

    def subscriber_exists(self, user_id):
        # Проверяем, есть ли уже юзер в базе
        with self.connection:
            result = self.cursor.execute('SELECT * FROM subscribers WHERE user_id = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, username, currency_type):
        # Добавляем нового подписчика
        with self.connection:
            self.cursor.execute("INSERT INTO subscribers (`user_id`, 'name', 'currency') VALUES(?,?,?)", (user_id,
                                                                                                          username,
                                                                                                          currency_type))
            self.connection.commit()

    def un_subscriber(self, user_id):
        with self.connection:
            self.cursor.execute('DELETE FROM subscribers WHERE user_id =?', (user_id,)).fetchall()
            self.connection.commit()

    def update_sub_number(self, user_id, phone_number):
        # Обновляем статус подписки пользователя
        with self.connection:
            return self.cursor.execute("UPDATE subscribers SET `phone` = ? WHERE `user_id` = ?", (phone_number,
                                                                                                  user_id))

    def update_currency(self, user_id, currency_type):
        # Обновляем тип валюты
        with self.connection:
            return self.cursor.execute("UPDATE subscribers SET `currency` = ? WHERE `user_id` = ?", (currency_type,
                                                                                                     user_id))

    def close(self):
        # Закрываем соединение с БД
        self.connection.close()
