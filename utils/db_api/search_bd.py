import sqlite3
import requests
import keyboards.default as kb


r = requests.Session()
currency = ['', 'USD', 'EUR', 'RUB', 'UAH', 'BYN']


async def get_subscriptions(message):
    conn = sqlite3.connect('catbd.db')
    cursor = conn.cursor()
    subscribers = cursor.execute("SELECT * FROM subscribers").fetchall()
    conn.close()
    iteration = 0
    await message.answer(f'Колличество подписчиков: {len(subscribers)}')
    for subscribe in subscribers[-5:]:

        await message.answer(f'ID Пользователя: {subscribe[1]}\n'
                             f'Ник: @{subscribe[2]}\n'
                             f'Телефон: {subscribe[3]}',
                             reply_markup=kb.admins_kb)



async def subscriptions():
    conn = sqlite3.connect('catbd.db')
    cursor = conn.cursor()
    users = cursor.execute("SELECT * FROM subscribers").fetchall()
    conn.close()
    return users


async def get_number(user_id):
    connection = sqlite3.connect('catbd.db')
    cursor = connection.cursor()
    result = cursor.execute('SELECT * FROM subscribers WHERE user_id = ?', (user_id,)).fetchall()
    connection.close()
    return result[0]



