from aiogram import types
import keyboards.default as kb
import keyboards.inline as inl
import requests
import json
from data.config import KEY, USER_AGENT


r = requests.Session()
currency = ['', 'USD', 'EUR', 'RUB', 'UAH', 'BYN']


# Поиск катализатора по параметрам авто
async def get_cat(message, data, number):
    brands_id = await get_brand()
    for brand in brands_id:
        if data[0] == brand[1]:
            count = brand[0]
            break
    else:
        count = ''
    responce_brand = r.post(
        'https://debug.catalyst.by/json.php',
        data={
            'command': 'search',
            'phone': str(number[3]),
            'key': KEY,
            'currID': str(number[4]),
            'brand': str(count),
            'model': str(data[1]),
            'engtype': str(data[2]),
            'size': str(data[3]),
            'cattype': '',
            'serial': '',
            'yearFirst': str(data[4]),
            'yearLast': ''
        },
        headers=USER_AGENT
    )
    json_data = responce_brand.json()
    count = json.dumps(json_data["count"])
    total = list(json_data['Database'].values())
    out = list(json_data['user'].values())
    if int(count) >= 1:
        for number in range(0, int(count)):
            result = list(json_data[str(number)].values())
            currency = list(json_data['user'].values())
            await get_resault(message, result, currency)

    else:
        await message.answer(
            f'Данного авто, нет в списке.\n'
            f'Попробуйте еще раз или обратитесь к нашему специалисту: \n'
            f'📩 @McConst', reply_markup=kb.greet_kb)
    await out_info(message, total, out)



async def get_catnumber(message: types.Message, data, number):
    global count
    if data[0] == '':
        count = ''
    else:
        brands_id = await get_brand()
        for brand in brands_id:
            if data[0] == brand[1]:
                count = brand[0]

    responce_brand = r.post('https://debug.catalyst.by/json.php',
                            data={
                                'command': 'search',
                                'phone': str(number[3]),
                                'key': KEY,
                                'currID': str(number[4]),
                                'brand': str(count),
                                'serial': str(data[1]),
                            },
                            headers=USER_AGENT
                            )

    json_data = responce_brand.json()
    count = json.dumps(json_data["count"])
    total = list(json_data['Database'].values())
    out = list(json_data['user'].values())
    if int(count) >= 1:
        for number in range(0, int(count)):
            result = list(json_data[str(number)].values())
            currency = list(json_data['user'].values())
            await get_resault(message, result, currency)

    else:
        await message.answer(
            f'Данного катализатора, нет в списке.\n'
            f'Попробуйте еще раз или обратитесь к нашему специалисту: \n'
            f'📩 @McConst', reply_markup=kb.greet_kb)
    await out_info(message, total, out)


#Инфо в личный кабинет
async def history_search(message, number):
    responce_brand = r.post('https://debug.catalyst.by/json.php', data={'command': 'getUserData',
                                                                        'phone': str(number[3]),
                                                                        'key': KEY

                                                                        }, headers=USER_AGENT)
    json_data = responce_brand.json()
    result = list(json_data['user'].values())
    await message.answer(
        f'<b>Тип подписки:</b> {result[3]}.\n'
        f'<b>Доступно поисков за день:</b> {result[4]}.\n'
        f'<b>Выполнено поисков за день:</b> {result[5]}.\n'
        f'\n<b>Время начала подписки:</b>\n{result[6]}.\n'
        f'\n<b>Время окончаниия подписки:</b> \n{result[7]}.\n'
        f'\n<b>Бесплатных поисков</b>\n'
        f'<b>После окончания подписки:</b> {result[8]}.\n',
        parse_mode='HTML',
        reply_markup=kb.cabinet_kb)
    await message.answer(
        f'<b>Ваша валюта для вывода цены:</b> {currency[int(number[4])]}',
        parse_mode='HTML',
        reply_markup=inl.inline_kb_val)


# Поиск id авто
async def get_brand():
    responce_brand = r.post('https://debug.catalyst.by/json.php',
                            data={
                                'command': 'getBrandID',
                                'key': KEY},
                            headers=USER_AGENT)
    brand = []
    json_data = responce_brand.json()
    count = json.dumps(json_data["count"])
    for number in range(0, int(count)):
        result = list(json_data[str(number)].values())
        brand.append(result)
    return brand


# Функция проверки вводных данных пользователем
async def search_bd(data, number, searchfield):
    global count, model, e_type
    if data[0] == '':
        count = ''
    else:
        brands_id = await get_brand()
        for brand in brands_id:
            if data[0] == brand[1]:
                count = brand[0]
    if len(data) == 1:
        model = ''
        e_type = ''
    elif len(data) == 2:
        model = data[1]
        e_type = ''
    elif len(data) == 3:
        e_type = data[2]
    responce_brand = r.post(f'https://debug.catalyst.by/serial.php?brand={count}&model={model}&engtype={e_type}'
                            f'&searchfield={searchfield}', data={'phone': str(number[3]),
                                                                 'key': KEY}, headers=USER_AGENT)
    json_data = responce_brand.json()
    base = []
    count = json.dumps(json_data["count"])
    if int(count) >= 1:
        result = list(json_data[f'{searchfield}'].values())
        for number in range(0, int(count)):
            if result[number] is None:
                continue
            else:
                base.append(result[number])
    return base


# Запрос ссылки на оплату в личный кабинет
async def account(number):
    responce_brand = r.post('https://debug.catalyst.by/json.php', data={'command': 'getAccountLink',
                                                                        'phone': str(number[3]),
                                                                        'key': KEY}, headers=USER_AGENT)
    json_data = responce_brand.json()
    url = json.dumps(json_data["url"])
    return url


# Вывод результатов поиска
async def get_resault(message, result, currency):
    global photo
    try:
        if result[5] is None:
            if 'g' in result[2]:
                result[2] = 'Бензин'
            elif 'd' in result[2]:
                result[2] = 'Дизель'
            else:
                result[2] = ''
            if result[13] is None:
                photo_jpg = '-'
                photo = "Фото: - ."
            else:
                photo_jpg = f'https://catalyst.by/img/{result[13]}'
                photo = 'Фото:'
            if result[14] is None:
                result[14] = '-'
            if result[7] is None:
                result[7] = '-'
            return await message.answer(
                f'<b>Марка:</b> {result[0]}. '
                f'<b>Модель:</b> {result[1]}.\n'
                f'<b>ДВС:</b> {result[3]} {result[2]}. '
                f'<b>Вес:</b> {result[8]}кг.\n'
                f'<b>Номер CAT:</b> {result[7]}.\n'
                f'<b>Цена катализатора:</b> {result[11]} {currency[11]}\n'
                f'<b>Тип катализатора:</b> {result[9]}.\n'
                f'<b>Год:</b> - . '
                f'<a href="{photo_jpg}"><b>{photo}</b></a>\n'
                f'<b>Примечание:</b> {result[14]}',
                parse_mode='HTML',
                reply_markup=kb.greet_kb
            )
        elif result[6] is None:
            if 'g' in result[2]:
                result[2] = 'Бензин'
            elif 'd' in result[2]:
                result[2] = 'Дизель'
            else:
                result[2] = ''
            if result[13] is None:
                photo_jpg = '-'
                photo = "Фото: - ."
            else:
                photo_jpg = f'https://catalyst.by/img/{result[13]}'
                photo = 'Фото:'
            if result[14] is None:
                result[14] = '-'
            if result[7] is None:
                result[7] = '-'
            return await message.answer(
                    f"<b>Марка:</b> {result[0]}. "
                    f'<b>Модель:</b> {result[1]}.\n'
                    f'<b>ДВС:</b> {result[3]} {result[2]}. '
                    f'<b>Вес:</b> {result[8]}кг.\n'
                    f'<b>Номер CAT:</b> {result[7]}.\n'
                    f'<b>Цена катализатора:</b> {result[11]} {currency[11]}\n'
                    f'<b>Тип катализатора:</b> {result[9]}.\n'
                    f'<b>Год:</b> {result[5]}. '
                    f'<a href="{photo_jpg}"><b>{photo}</b></a>\n'
                    f'<b>Примечание:</b> {result[14]}',
                    parse_mode='HTML',
                    reply_markup=kb.greet_kb
                )
        else:
            if 'g' in result[2]:
                result[2] = 'Бензин'
            elif 'd' in result[2]:
                result[2] = 'Дизель'
            else:
                result[2] = ''
            if result[13] is None:
                photo_jpg = '-'
                photo = "Фото: - ."
            else:
                photo_jpg = f'https://catalyst.by/img/{result[13]}'
                photo = 'Фото:'
            if result[14] is None:
                result[14] = '-'
            if result[7] is None:
                result[7] = '-'
            return await message.answer(
                f'<b>Марка:</b> {result[0]}. '
                f'<b>Модель:</b> {result[1]}.\n'
                f'<b>ДВС:</b> {result[3]} {result[2]}. '
                f'<b>Вес:</b> {result[8]}кг.\n'
                f'<b>Номер CAT:</b> {result[7]}.\n'
                f'<b>Цена катализатора:</b> {result[11]} {currency[11]}\n'
                f'<b>Тип катализатора:</b> {result[9]}.\n'
                f'<b>Год:</b> {result[5]}-{result[6]}. '
                f'<a href="{photo_jpg}"><b>{photo}</b></a>\n'
                f'<b>Примечание:</b> {result[14]}',
                parse_mode='HTML',
                reply_markup=kb.greet_kb
            )
    except:
        pass


# Вывод информации по колличеству доступных позиций
async def out_info(message, total, out):
    global subscribe

    if total[0] == total[1]:
        subscribe = 'Вам доступны все позиции.'
    elif total[1] < total[0] and out[3] != 'Guest':
        subscribe = 'Для полного доступа\n' \
                    'Продлите подписку в личном кабинете.'
    if out[3] == 'Guest':
        subscribe = 'Зарегистрируйтесь для полного доступа.'

    await message.answer(
        f'Поиск выполняется\n'
        f'по {total[1]} позиций из {total[0]}\n'
        f'{subscribe}'
    )


