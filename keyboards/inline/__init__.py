from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

inline_btn_1 = InlineKeyboardButton('Вернуться в главное меню ♻️', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

inline_btn_2 = InlineKeyboardButton('Пропустить ♻️', callback_data='button2')
inline_kb2 = InlineKeyboardMarkup().add(inline_btn_2)
inline_next = InlineKeyboardMarkup().add(inline_btn_1).add(inline_btn_2)

inline_btn_4 = InlineKeyboardButton('Пропустить ♻️', callback_data='button3')
inline_btn_3 = InlineKeyboardButton('catalyst.by', callback_data='registration',
                                    url='https://catalyst.by/registration.php?Language=2', )
inline_kb_registration = InlineKeyboardMarkup().add(inline_btn_3).add(inline_btn_4)

inline_btn_RUB = InlineKeyboardButton('RUB', callback_data='RUB')
inline_btn_EUR = InlineKeyboardButton('EUR', callback_data='EUR')
inline_btn_BYN = InlineKeyboardButton('BYN', callback_data='BYN')
inline_btn_USD = InlineKeyboardButton('USD', callback_data='USD')
inline_btn_UAH = InlineKeyboardButton('UAH', callback_data='UAH')
inline_kb_val = InlineKeyboardMarkup().row(inline_btn_RUB, inline_btn_EUR, inline_btn_BYN,
                                           inline_btn_USD, inline_btn_UAH)
