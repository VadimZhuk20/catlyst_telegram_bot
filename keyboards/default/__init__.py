from aiogram.types import ReplyKeyboardMarkup
from aiogram import types


buttons_admin = ['Рассылка 📩',
                 'Подписчики 👥',
                 'Меню пользователя 📲']

buttons = ['Контакты 🗃️',
           'Личный кабинет 🚪',
           'Цена по номеру 📝',
           'Цена по марке 🚗']

button_brand = ["BMW", "Chery", "Chevrolet", 'Chrysler / Jeep', "Daewoo", "Daihatsu", "Dodge", "Eminox", "Ferrari",
                'Fiat / Alfa Romeo', 'Ford / Jaguar', "Geely", "Hino", "HJS", "Honda", 'Hyundai-KIA', "Isuzu", "Iveco",
                "Lancia", "LDV", "Lifan", "Maserati", "Mazda", "Mercedes", "Mitsubishi", "Nissan", "Opel", "Perodua",
                "Proton", "PSA", "Renault", "Rolls Royce", 'Rover / Landrover', "Saab", "Seat", "Sevel", "Skoda", "Smart",
                "SsangYong", "Subaru", "Suzuki", "Tata", "Toyota", "Unidentified", "VAG", "VAZ", "Volvo", "Walker",
                "Great Wall", "Pontiac", "GAZ", "Manitou", "Aftermarket", "Cadillac", "DAF", "Leibherr", "John Deere",
                "Buick", "UAZ", "Bentley", "MAN", "Iran Khodro", "Lincoln", "Hummer", "Scania", "Porsche", "Yamaha",
                "McLaren"]

button_exit = ['Вернуться в главное меню ♻️', ]

button_next = ['Пропустить ♻️', ]

button_cabinet = ['Поддержка 🔔', 'Подписка ✔']

button_un_subscribe = ["Отписаться 🆑", ]

button_yes = ['Да', ]

button_subscribe = ['Пройти регистрацию ✔']

button_paid_subscription = ['Подписаться на сайте']

button_type_engine = ['Бензин', 'Дизель']

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(*buttons)
subscribe_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(*button_subscribe)
admins_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(*buttons_admin)
brand_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=3).row(*button_next).row(
    *button_exit).add(
    *button_brand)

exit_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1).add(
    *button_paid_subscription).add(*button_un_subscribe).add(*button_exit)

type_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(*button_type_engine).add(
    *button_next)

cabinet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(*button_cabinet).row(
    *button_exit)

unsubscribe_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2).add(*button_yes).add(
    *button_exit)

registration_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    types.KeyboardButton('Отправить свой контакт ☎️',
                         request_contact=True))