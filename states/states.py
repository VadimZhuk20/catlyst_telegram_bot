from aiogram.dispatcher.filters.state import StatesGroup, State


class Test(StatesGroup):
    Brand = State()
    Model = State()
    Type = State()
    Engine = State()
    Year = State()
    Brand_number = State()
    Number = State()
    Message = State()
    Phone = State()


