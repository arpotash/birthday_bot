from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command, StateFilter
from db import cur, conn
from aiogram import types
from aiogram.fsm.context import FSMContext

auth_router = Router()

class RegisterAccount(StatesGroup):
    first_name = State()
    last_name = State()
    will_be = State()
    comment = State()


@auth_router.message(StateFilter(None), CommandStart())
async def register(message: types.Message, state: FSMContext):
    await message.answer(
        f'Привет!\n\n'
        f'Если ты получил ссылку на бота и читаешь это сообщение, значит ты точно знаешь одного из этих людей: '
        f'Поташов Артём, Малахов Павел, Романов Алексей.\n\n'
        f'Не буду лить много воды, все четко и по порядку.\n\n'
        f'Дата: 12-13 июля\n\n'
        f'Дресс-код: [Укажите дресс-код]\n\n'
        f'Пожелания по подаркам: виш-листа в этот раз не будет, идеальный подарок - деньги :)\n\n'
        f'Как добраться: информация есть в разделе "Локации"\n\n'
        f'По всем пожеланиям можно также написать в разделе "Wish"\n\n'
        f'Осталось только зарегистрироваться и готовиться к празднику, до встречи!'
    )
    await message.answer("Введи имя", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegisterAccount.first_name)


@auth_router.message(RegisterAccount.first_name, F.text)
async def add_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Теперь фамилию")
    await state.set_state(RegisterAccount.last_name)


@auth_router.message(RegisterAccount.last_name, F.text)
async def add_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    options = ['Буду', 'Точно не знаю', 'Не смогу']
    keyboard_markup = [
        [
            types.InlineKeyboardButton(
                text=option,
                callback_data=f'option_{options.index(option)}'
            )
        ]
        for option in options
    ]
    markup = types.InlineKeyboardMarkup(inline_keyboard=keyboard_markup)
    await message.answer("А ты будешь на празднике?", reply_markup=markup)
    await state.set_state(RegisterAccount.will_be)

@auth_router.message(RegisterAccount.will_be, F.text)
@auth_router.callback_query(lambda query: query.data.startswith('option_'))
async def process_option(callback_query: types.CallbackQuery, state: FSMContext):
    selected_option_index = int(callback_query.data.split('_')[1])
    options = ['Буду', 'Точно не знаю', 'Не смогу']
    selected_option = options[selected_option_index]
    await state.update_data(will_be=selected_option)
    await callback_query.message.answer("Если будешь +1, пиши +1, если есть другие комментарии, тоже пиши")
    await state.set_state(RegisterAccount.comment)


@auth_router.message(RegisterAccount.comment, F.text)
async def add_comment(message: types.Message, state: FSMContext):
    try:
        await state.update_data(comment=message.text)
        data = await state.get_data()
        values = tuple(data for data in data.values())

        insert_account_query = f'insert into account (first_name, last_name, will_be, comment) values (%s, %s, %s, %s)'

        cur.execute(insert_account_query, values)
        conn.commit()
    except Exception as e:
        conn.rollback()
        await message.answer("Нене, зарегистрироваться можно только 1 раз")
    else:
        await message.answer("Регистрация завершена, теперь можно посмотреть детали")
    finally:
        await state.clear()