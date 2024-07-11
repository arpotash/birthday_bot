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

class CreateWish(StatesGroup):
    wish = State()

class AdminAccount(StatesGroup):
    password = State()

@auth_router.message(Command(commands='members'))
async def get_members_count(message: types.Message, state: FSMContext):
    count_member_query = 'select count(*) from account'
    cur.execute(count_member_query)
    members_count = cur.fetchall()
    formatted_members = "Количество участников {} из 30".format(members_count[0][0])
    await message.answer(formatted_members)
    await message.answer('Более подробная информация доступна организаторам, введите пароль:')
    await state.set_state(AdminAccount.password)



@auth_router.message(AdminAccount.password, F.text)
async def get_members(message: types.Message, state: FSMContext):
    if message.text == "/members":
        await state.clear()
        return await get_members_count(message, state)
    if message.text == "/start":
        await state.clear()
        return await register(message, state)

    if message.text == 'hiranuka':
        all_member_query = 'select first_name, last_name, will_be, comment from account order by will_be'
        cur.execute(all_member_query)
        members = cur.fetchall()
        formatted_members = "\n".join([f"{member[0]} {member[1]} {member[2]}" for member in members])
        await message.answer(f'Полный список участников:\n{formatted_members}')
    else:
        await message.answer('Неверный пароль!')



@auth_router.message(Command(commands="location"))
async def get_location(message: types.Message, state: FSMContext):
    await state.clear()
    media = []
    photo_paths = [
        'photo_6.png',
        'photo_7.png',
        'photo_3.png',
        'photo_2.png',
        'photo_4.png',
        'photo_5.png',
        'photo_6.png'
    ]
    for file in photo_paths:
        photo = types.InputMediaPhoto(media=types.FSInputFile(file))
        media.append(photo)

    await message.answer_media_group(media=media)
    await message.answer(
        "🏡 **Функциональный коттедж** с 6-ю изолированными спальнями, 2-мя игровыми залами, а также большим банкетным залом и просторной кухней.\n"
        "Прекрасное место в 20 минутах от КАДа и 5 минут от ЗСД, для проведения праздников, различных мероприятий и просто спокойного отдыха.\n\n"
        "🔥 **Отапливается**: радиаторами и теплым полом, в летний период работают кондиционеры, приглашаем не только взрослых, но и самых маленьких гостей.\n\n"
        "📍 **На первом этаже**:\n"
        "- Большой банкетный зал на 50 человек с профессиональным звуком, светом и караоке.\n"
        "- 2 спальни и 2 санузла.\n\n"
        "📍 **На втором этаже**:\n"
        "- Отдельная СПА-зона с сауной, покерным столом и мягким диваном.\n"
        "- Большая комфортная кухня с печью на дровах и открытым камином для барбекю.\n"
        "- 2 игровых зала с круглым столом для игры в мафию и профессиональными покерными столами.\n"
        "- 4 спальни и 3 санузла.\n\n"
        "🚗 **На закрытой территории**: большая парковочная зона."
        "Адрес - Ленинградская обл., Всеволожский р-н, Юкковское сельское поселение, \n\n"
        "СНТ Терра-Выборгское, Лазаревская ул., 20, Выборгское шоссе, 17 км\n\n"
    )



@auth_router.message(StateFilter(None), CommandStart())
async def register(message: types.Message, state: FSMContext):
    await message.answer(
        f'Привет!\n\n'
        f'Если ты получил ссылку на бота и читаешь это сообщение, значит ты точно знаешь одного из этих людей: '
        f'Поташов Артём, Малахов Павел, Романов Алексей.\n\n'
        f'Не буду лить много воды, все четко и по порядку.\n\n'
        f'Дата: 13-14 июля.\n\n'
        f'Время сбора гостей: 16:00.\n\n'
        f'Адрес - Ленинградская обл., Всеволожский р-н, Юкковское сельское поселение, \n\n'
        f'СНТ Терра-Выборгское, Лазаревская ул., 20, Выборгское шоссе, 17 км\n\n'
        f'Дресс-код: свободный стиль\n\n'
        f'Пожелания по подаркам: виш-листа в этот раз не будет, идеальный подарок - деньги :)\n\n'
        f'Как добраться: информация есть в разделе "Локации"\n\n'
        f'Осталось только зарегистрироваться и готовиться к празднику, до встречи!'
    )
    await message.answer("Введи имя", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegisterAccount.first_name)


@auth_router.message(RegisterAccount.first_name, F.text)
async def add_first_name(message: types.Message, state: FSMContext):
    if message.text == "/start":
        await state.clear()
        return await register(message, state)

    if message.text == "/members":
        await state.clear()
        return await get_members_count(message, state)

    await state.update_data(first_name=message.text)
    await message.answer("Теперь фамилию")
    await state.set_state(RegisterAccount.last_name)


@auth_router.message(RegisterAccount.last_name, F.text)
async def add_last_name(message: types.Message, state: FSMContext):
    if message.text == "/start":
        await state.clear()
        return await register(message, state)

    if message.text == "/members":
        await state.clear()
        return await get_members_count(message, state)

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
    if callback_query.message.text == "/start":
        await state.clear()
        return await register(callback_query.message, state)

    selected_option_index = int(callback_query.data.split('_')[1])
    options = ['Буду', 'Точно не знаю', 'Не смогу']
    selected_option = options[selected_option_index]
    await state.update_data(will_be=selected_option)
    await state.update_data(comment=callback_query.message.text)
    data = await state.get_data()
    select_account_query = (
        f'select will_be '
        f'from account '
        f'where first_name = %s and last_name = %s'
    )
    cur.execute(select_account_query, (data.get("first_name"), data.get("last_name")))
    account = cur.fetchone()

    if account and account[0] == data.get("will_be"):
        await callback_query.message.answer("Может другой ответ выберешь, этот уже был!")
        return await get_location(callback_query.message, state)

    if account and account[0] != data.get("will_be"):
        update_account_query = (
            'UPDATE account SET will_be = %s WHERE first_name = %s AND last_name = %s'
        )
        cur.execute(update_account_query, (data.get("will_be"), data.get("first_name"), data.get("last_name")))
        conn.commit()
        await callback_query.message.answer("Ок, это твой выбор, я с ним согласен!")
        return await get_location(callback_query.message, state)
    else:
        values = tuple(data for data in data.values())
        insert_account_query = f'insert into account (first_name, last_name, will_be, comment) values (%s, %s, %s, %s)'

        cur.execute(insert_account_query, values)
        conn.commit()

        await callback_query.message.answer(
            "Регистрация завершена, теперь можно посмотреть детали, "
            "если есть какие-либо пожелания, можешь написать одному из организаторов лично"
        )
        return await get_location(callback_query.message, state)
