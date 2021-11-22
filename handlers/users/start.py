from aiogram.types import ContentType
from data.config import ADMINS
from aiogram import executor
from states.states import Test
from aiogram.dispatcher import FSMContext
from utils.db_api.subscriber import SQLighter
from loader import *
from utils.db_api.search_bd import *
from utils.redis.post import *


data = []
db = SQLighter()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if message.chat.id in ADMINS:
        await bot.send_message(message.from_user.id, 'Здраствуйте,{0.full_name}!\n'
                                                     'Меню Администратора:'
                               .format(
            message.from_user), reply_markup=kb.admins_kb)

    else:
        if not db.subscriber_exists(message.from_user.id):
            await bot.send_message(message.from_user.id, 'Добрый день, {0.full_name}!\n'
                                                         'Мы молодой проект и хотим помочь людям найти'
                                                         ' лучшие цены, на отработанные катализаторы. ™\n'
                                                         'Для сотрудничества и предложений напишите в поддержку.📜\n'

                                                         '\nПройдите регистрацию, что бы получить доступ ✔:'
                                   .format(
                message.from_user),
                                   reply_markup=kb.subscribe_kb()
                                   )

            # Команда регистрации
            @dp.message_handler(lambda message: message.text == 'Пройти регистрацию ✔')
            async def subscribe(message: types.Message):
                if not db.subscriber_exists(message.from_user.id):
                    db.add_subscriber(message.from_user.id, message.from_user.username, '5')

                await message.answer('Регистрация номера телефона 📞',
                                     reply_markup=kb.registration_kb)
                await Test.Phone.set()

            @dp.message_handler(lambda message: message.text == "Отписаться")
            async def subscribe(message: types.Message):
                if db.subscriber_exists(message.from_user.id):
                    db.un_subscriber(message.from_user.id)

                await message.answer(
                    "Вы успешно отписались!")
        else:
            await bot.send_message(message.from_user.id, 'Здраствуйте, {0.full_name}!\n'

                                                         'Выберете действие:'
                                   .format(
                message.from_user), reply_markup=kb.greet_kb)


# Обработчик кнопки выбора типа подписки
@dp.message_handler(lambda message: message.text == 'Подписка ✔')
async def subscribers(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберете подписку:'
                           .format(
        message.from_user), reply_markup=kb.exit_kb)

    # Кнопка Платной подписка
    @dp.message_handler(lambda message: message.text == 'Подписаться на сайте')
    async def subscribe(message: types.Message):
        number = await get_number(message.from_user.id)
        acc = await account(number)
        acc.replace('"', '')
        href = f'<a href={acc}>Оплата в личном кабинете</a>'
        await message.answer(
            href,
            parse_mode='HTML',
            reply_markup=inl.inline_kb1)

    # Возврат в главное меню из платной подписки
    @dp.callback_query_handler(lambda c: c.data == 'button1')
    async def process_callback_paid(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Выберете действие:', reply_markup=kb.greet_kb)

    # Кнопка отписки
    @dp.message_handler(lambda message: message.text == "Отписаться 🆑")
    async def subscribe(message: types.Message):
        if message.from_user.id in ADMINS:
            await message.answer('Решил отписаться?\n'
                                 'Давай работай !', reply_markup=kb.admins_kb)
        else:
            await message.answer(
                "Вы уверены?", reply_markup=kb.unsubscribe_kb)

            @dp.message_handler(lambda message: message.text == "Да")
            async def subscribe(message: types.Message):
                await message.answer('Вы успешно отписались!')
                db.un_subscriber(message.from_user.id)

            @dp.message_handler(lambda message: message.text == "Вернуться в главное меню ♻️")
            async def subscribe(message: types.Message):
                await message.answer('Выберете действие:', reply_markup=kb.greet_kb)

    @dp.message_handler(lambda message: message.text == 'Вернуться в главное меню ♻️')
    async def subscribers(message: types.Message):
        await bot.send_message(message.from_user.id, 'Выберете действие:'
                               .format(
            message.from_user), reply_markup=kb.greet_kb)


async def cabbinet(message: types.Message):
    number = get_number(message.from_user.id)
    catlyst = await account(number)
    return catlyst


# Обработчик кнопки номер катализатора
@dp.message_handler(lambda message: message.text == 'Цена по номеру 📝')
async def button_number(message: types.Message):
    await bot.send_message(message.from_user.id, 'Выберете марку авто:',
                           reply_markup=kb.brand_kb)
    await Test.Brand_number.set()


# Обработчик кнопки Сдать катализатор
@dp.message_handler(lambda message: message.text == 'Контакты 🗃️')
async def button_pass(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Пункт приема катализаторов:\n'
                           'УП "УНИДРАГМЕТ БГУ"\n'
                           'г.Минск, ул.Aкадемика Курчатова, 1\n'
                           '\nПриемная:\n'
                           '+375 (17) 398-38-81 (unidragmet@tut.by)\n'
                           '\nОтдел автокатализаторов:\n'
                           '(Telegram,Viber,WhatsApp):\n'
                           '+375291868018 (tarazevich@bsu.by)\n'
                           '\nТехнический администратор:\n'
                           'Viber/WhatsApp/Telegram:\n'
                           '+375257205113\n'
                           'e-mail: mycatalyst@yandex.ru\n',
                           reply_markup=kb.greet_kb)


# Обработчик кнопки цена по марке авто
@dp.message_handler(lambda message: message.text == 'Цена по марке 🚗')
async def button_brand(message: types.Message):
    await message.answer("Выберете марку авто:",
                         reply_markup=kb.brand_kb)
    await Test.Brand.set()


# Обработчик кнопки поддержка
@dp.message_handler(lambda message: message.text == 'Поддержка 🔔')
async def button_pass(message: types.Message):
    await bot.send_message(message.from_user.id, 'Напишите нашему специалисту ваше предложение: 📩  @McConst',
                           reply_markup=kb.greet_kb)


# Обработчик кнопки просмотра колличества подписчиков
@dp.message_handler(lambda message: message.text == 'Подписчики 👥')
async def button_subscribers(message: types.Message):
    await get_subscriptions(message)


# Кнопка рассылки по подписчикам бота
@dp.message_handler(lambda message: message.text == 'Рассылка 📩')
async def button_mail(message: types.Message):
    await message.answer("Введите текст рассылки:",
                         reply_markup=inl.inline_kb1)
    await Test.Message.set()


# Кнопка пользователя: переход в личный кабинет
@dp.message_handler(lambda message: message.text == 'Личный кабинет 🚪')
async def button_personal_area(message: types.Message):
    number = await get_number(message.from_user.id)
    await history_search(message, number)

    @dp.callback_query_handler(lambda c: c.data == 'RUB')
    async def process_callback_rub(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        db.update_currency(callback_query.from_user.id, '3')
        number = await get_number(message.from_user.id)
        await message.answer(f'Ваша валюта для вывода цены: {currency[int(number[4])]}')

    @dp.callback_query_handler(lambda c: c.data == 'EUR')
    async def process_callback_eur(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        db.update_currency(callback_query.from_user.id, '2')
        number = await get_number(message.from_user.id)
        await message.answer(f'Ваша валюта для вывода цены: {currency[int(number[4])]}')

    @dp.callback_query_handler(lambda c: c.data == 'BYN')
    async def process_callback_byn(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        db.update_currency(callback_query.from_user.id, '5')
        number = await get_number(message.from_user.id)
        await message.answer(f'Ваша валюта для вывода цены: {currency[int(number[4])]}')

    @dp.callback_query_handler(lambda c: c.data == 'USD')
    async def process_callback_usd(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        db.update_currency(callback_query.from_user.id, '1')
        number = await get_number(message.from_user.id)
        await message.answer(f'Ваша валюта для вывода цены: {currency[int(number[4])]}')

    @dp.callback_query_handler(lambda c: c.data == 'UAH')
    async def process_callback_uah(callback_query: types.CallbackQuery):
        await bot.answer_callback_query(callback_query.id)
        db.update_currency(callback_query.from_user.id, '4')
        number = await get_number(message.from_user.id)
        await message.answer(f'Ваша валюта для вывода цены: {currency[int(number[4])]}')

    # Обработчик кнопки возврата в главное меню
    @dp.message_handler(lambda message: message.text == 'Вернуться в главное меню ♻️')
    async def button_brand(message: types.Message):
        await message.answer("Выберете действие:",
                             reply_markup=kb.greet_kb)


# Кнопка вызова меню пользователя из меню администратора
@dp.message_handler(lambda message: message.text == 'Меню пользователя 📲')
async def button_pass(message: types.Message):
    await bot.send_message(message.from_user.id, "Меню пользователя:",
                           reply_markup=kb.greet_kb)


# Обработчик кнопки выхода из состояния "Вернуться в главное меню"
@dp.callback_query_handler(lambda c: c.data == 'button1', state=Test.Brand)
async def process_callback_button1(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.from_user.id in ADMINS:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, 'Выберете действие:',
                               reply_markup=kb.greet_kb)
        await state.finish()
        data.clear()


# Обработчик кнопки выхода из состояния "Вернуться в главное меню"
@dp.callback_query_handler(lambda c: c.data == 'button1', state=Test.Year)
async def process_callback_button2(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете действие:',
                           reply_markup=kb.greet_kb)
    await state.finish()
    data.clear()


# Обработчик кнопки выхода из состояния "Вернуться в главное меню"
@dp.callback_query_handler(lambda c: c.data == 'button1', state=Test.Engine)
async def process_callback_button3(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете действие:',
                           reply_markup=kb.greet_kb)
    await state.finish()
    data.clear()


# Обработчик кнопки выхода из состояния "Вернуться в главное меню"
@dp.callback_query_handler(lambda c: c.data == 'button1', state=Test.Type)
async def process_callback_button4(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете действие:',
                           reply_markup=kb.greet_kb)
    await state.finish()
    data.clear()


# Обработчик кнопки выхода из состояния "Вернуться в главное меню"
@dp.callback_query_handler(lambda c: c.data == 'button1', state=Test.Number)
async def process_callback_button4(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете действие:', reply_markup=kb.greet_kb)
    await state.finish()
    data.clear()


# Обработчик кнопки выхода из состояния "Вернуться в главное меню"
@dp.callback_query_handler(lambda c: c.data == 'button1', state=Test.Type)
async def process_callback_button4(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете действие:', reply_markup=kb.greet_kb)
    await state.finish()
    data.clear()


# Обработчик кнопки выхода из состояния "Вернуться в главное меню"
@dp.callback_query_handler(lambda c: c.data == 'button1', state=Test.Model)
async def process_callback_button4(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете действие:', reply_markup=kb.greet_kb)
    await state.finish()
    data.clear()


# Обработчик кнопки выхода из состояния "Вернуться в главное меню"
@dp.callback_query_handler(lambda c: c.data == 'button1', state=Test.Engine)
async def process_callback_button4(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете действие:', reply_markup=kb.greet_kb)
    await state.finish()
    data.clear()


# Обработчик кнопки выхода из состояния "Вернуться в главное меню"
@dp.callback_query_handler(lambda c: c.data == 'button1', state=Test.Year)
async def process_callback_button4(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете действие:', reply_markup=kb.greet_kb)
    await state.finish()
    data.clear()


# Обработчик кнопки "пропустить"
@dp.callback_query_handler(lambda c: c.data == 'button2', state=Test.Model)
async def process_callback_button4(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете тип ДВС:',
                           reply_markup=kb.type_kb)
    data.append('')
    await Test.Type.set()


# Обработчик кнопки "пропустить"
@dp.callback_query_handler(lambda c: c.data == 'button2', state=Test.Engine)
async def process_callback_button5(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Год авто: 1999, 2005, 2018...',
                           reply_markup=inl.inline_next
                           )
    data.append('')
    await Test.Year.set()


# Обработчик кнопки "пропустить"
@dp.callback_query_handler(lambda c: c.data == 'button2', state=Test.Year)
async def process_callback_button6(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    data.append('')
    if data[2] == 'g':
        type_dvs = 'Бензин'
    elif data[2] == 'd':
        type_dvs = 'Дизель'
    else:
        type_dvs = ''
    await bot.send_message(callback_query.from_user.id, f'Параметры поиска:\n'
                                                        f'{data[0]}/ {data[1]}/ {type_dvs}/ {data[3]}/ {data[4]}\n'
                                                        f'Результаты поиска:',
                           reply_markup=kb.greet_kb)
    await state.finish()
    number = await get_number(callback_query.from_user.id)
    await get_cat(callback_query.message, data, number)
    data.clear()


# Обработчик кнопки выхода из состояния "Вернуться в главное меню"
@dp.callback_query_handler(lambda c: c.data == 'button1', state=Test.Message)
async def process_callback_button4(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете действие:', reply_markup=kb.admins_kb)
    await state.finish()


# Обработчик регистрации
@dp.callback_query_handler(lambda c: c.data == 'registration', state=Test.Phone)
async def process_callback_button2(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)

    await state.finish()


# Обработчик кнопки 'пропустить' в меню регистрации
@dp.callback_query_handler(lambda c: c.data == 'button3')
async def process_callback_button2(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, 'Выберете действие:',
                           reply_markup=kb.greet_kb)


# Первое состояние пользователя (выбор марки авто)
@dp.message_handler(state=Test.Brand)
async def answer_brand(message: types.Message, state: FSMContext):
    answer = message.text
    if message.text == 'Вернуться в главное меню ♻️':
        await message.answer('Выберете действие:',
                             reply_markup=kb.greet_kb)
        await state.finish()
    elif message.text == 'Пропустить ♻️':
        data.append('')
        searchfield = 'model'
        number = await get_number(message.from_user.id)
        examination = await search_bd(data, number, searchfield)
        await message.answer(f"Введите модель авто:\n"
                             f"\nПример:\n"
                             f"{examination}\n"
                             f"\nЛибо пропустите параметр.",
                             reply_markup=inl.inline_next)
        await Test.next()
    else:
        brands = []
        brands_id = await get_brand()
        for brand in brands_id:
            brands.append(brand[1])
        if answer in brands:
            data.append(answer)
            searchfield = 'model'
            number = await get_number(message.from_user.id)
            examination = await search_bd(data, number, searchfield)
            await message.answer(f"Введите модель авто:\n"
                                 f"\nПример:\n"
                                 f"{examination}\n"
                                 f"\nЛибо пропустите параметр.",
                                 reply_markup=inl.inline_next)
            await Test.next()
        else:
            await message.answer('Вы ввели неверную марку авто', reply_markup=kb.brand_kb)


# Второе состояние пользователя ввод модели(не обязательное)
@dp.message_handler(state=Test.Model)
async def answer_year(message: types.Message):
    # await message.answer('k', reply_markup=kb.inline_next)
    answer = message.text
    data.append(answer)
    searchfield = 'engine_size'
    number = await get_number(message.from_user.id)
    examination = await search_bd(data, number, searchfield)
    if len(examination) >= 1:
        await message.answer('Выберете тип ДВС:', reply_markup=kb.type_kb)
        await Test.next()
    else:
        await message.answer('Такой модели нет в базе.')
        data.pop(1)


# Третье состояние пользователя (выбор типа двс)
@dp.message_handler(state=Test.Type)
async def answer_type(message: types.Message):
    answer = message.text
    if message.text == 'Пропустить ♻️':
        data.append(' ')
        await message.answer('Объём двс: 1.5, 1.8, 2.0...',
                             reply_markup=inl.inline_next)
        await Test.next()
    else:
        if answer == 'Бензин':
            data.append('g')
            searchfield = 'engine_size'
            number = await get_number(message.from_user.id)
            examination = await search_bd(data, number, searchfield)
            if len(examination) >= 1:
                await message.answer(f'Пример ДВС:{examination}',
                                     reply_markup=inl.inline_next)
                await Test.next()
            else:
                await message.answer(f'Пример: 1.6, 2.0, 2.5...',
                                     reply_markup=inl.inline_next)
                await Test.next()

        elif answer == 'Дизель':
            data.append('d')
            searchfield = 'engine_size'
            number = await get_number(message.from_user.id)
            examination = await search_bd(data, number, searchfield)
            if len(examination) >= 1:
                await message.answer(f'Пример ДВС:{examination}',
                                     reply_markup=inl.inline_next)
                await Test.next()
            else:
                await message.answer(f'Пример: 1.6, 2.0, 2.5...',
                                     reply_markup=inl.inline_next)
                await Test.next()
        else:
            await message.answer('Неверный тип авто!', reply_markup=kb.type_kb)


# Четвертое состояние пользователя (ввод объема двс)
@dp.message_handler(state=Test.Engine)
async def answer_engine(message: types.Message):
    answer = message.text
    if answer.count('.') == 1:
        data.append(answer)
        await message.answer("Год выпуска авто.\n"
                             "(Пример:1990, 2005, 2017...):",
                             reply_markup=inl.inline_next)
        await Test.next()
    else:
        await message.answer('Введена неверная информация ‼')


# Пятое состояние пользователя (ввод года авто)
@dp.message_handler(state=Test.Year)
async def answer_year(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.isalnum() and len(answer) == 4:
        data.append(answer)
        if data[2] == 'g':
            type_dvs = 'Бензин'
        else:
            type_dvs = 'Дизель'
        await message.answer(f'Параметры поиска:\n'
                             f'{data[0]} / {data[1]} / {type_dvs} / {data[3]} / {data[4]}\n'
                             f'Результаты поиска:',
                             reply_markup=kb.greet_kb)
        await state.finish()
        number = await get_number(message.from_user.id)
        await get_cat(message, data, number)

        data.clear()

    else:
        await message.answer('Введена неверная информация ‼')


# Первое состояние пользователя(поиск по номеру)(Выбор Брэнда)
@dp.message_handler(state=Test.Brand_number)
async def answer_number(message: types.Message, state: FSMContext):
    if message.text == 'Вернуться в главное меню ♻️':
        await message.answer('Выберете действие:',
                             reply_markup=kb.greet_kb)
        await state.finish()
    elif message.text == 'Пропустить ♻️':
        data.append('')
        await message.answer('Введите номер катализатора 🔢:')
        await Test.next()
    else:
        answer = message.text
        brands = []
        brands_id = await get_brand()
        for brand in brands_id:
            brands.append(brand[1])
        if answer in brands:
            data.append(answer)
            searchfield = 'serial'
            number = await get_number(message.from_user.id)
            examination = await search_bd(data, number, searchfield)
            if len(examination) >= 1:
                await message.answer(f'Введите номер катализатора 🔢:\n'
                                     f'\nВозможные номера {examination}')
                await Test.next()
            else:
                await message.answer(f'Введите номер катализатора 🔢:')
                await Test.next()
        else:
            await message.answer('Вы ввели неверную марку авто', reply_markup=kb.brand_kb)


# Второе состояние пользователя(поиск по номеру)(Ввод номера кат)
@dp.message_handler(state=Test.Number)
async def answer_number(message: types.Message, state: FSMContext):
    answer = message.text
    data.append(answer)
    await message.answer('Спасибо за ответы!\n'
                         'Результаты поиска:', reply_markup=kb.greet_kb)

    number = await get_number(message.from_user.id)
    await get_catnumber(message, data, number)
    await state.finish()
    data.clear()


# Рассылка фото
@dp.message_handler(content_types=['photo'], state=Test.Message)
async def answer_message(message: types.Message, state: FSMContext):
    photo_id = message.photo[0].file_id
    subscribers = await subscriptions()
    for subscriber in subscribers:
        if subscriber[1] in ADMINS:
            await bot.send_photo(subscriber[1], photo_id, reply_markup=kb.admins_kb)
        else:
            await bot.send_message(subscriber[1], photo_id)

    await state.finish()


# Рассылка сообщений подписчикам
@dp.message_handler(state=Test.Message)
async def answer_message(message: types.Message, state: FSMContext):
    answer = message.text
    subscribers = await subscriptions()
    for subscriber in subscribers:
        if subscriber[1] in ADMINS:
            await bot.send_message(subscriber[1], answer, reply_markup=kb.admins_kb)
        else:
            await bot.send_message(subscriber[1], answer)

    await state.finish()


# Обработка номера телефона
@dp.message_handler(state=Test.Phone, content_types=ContentType.CONTACT)
async def phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number

    await state.finish()
    db.update_sub_number(message.from_user.id, phone_number)
    await bot.send_message(message.from_user.id, 'Перейдите по ссылке для регистрации \n'
                                                 'в личном кабинете сайта 📲\n'
                                                 'Если вы уже зарегестрированы\n'
                                                 'на сайте 📱\n'
                                                 'Нажмите кнопку "Пропустить"',
                           reply_markup=inl.inline_kb_registration)


if __name__ == '__main__':
    executor.start_polling(dp)
