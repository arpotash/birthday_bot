from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db import cur, conn
from aiogram.fsm.state import State, StatesGroup

router = Router()


class RegisterAccount(StatesGroup):
    first_name = State()
    last_name = State()
    will_be = State()
    comment = State()


class CreateWish(StatesGroup):
    wish = State()


@router.message(StateFilter(None), CommandStart())
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


@router.message(RegisterAccount.first_name, F.text)
async def add_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Теперь фамилию")
    await state.set_state(RegisterAccount.last_name)


@router.message(RegisterAccount.last_name, F.text)
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

@router.message(RegisterAccount.will_be, F.text)
@router.callback_query(lambda query: query.data.startswith('option_'))
async def process_option(callback_query: types.CallbackQuery, state: FSMContext):
    selected_option_index = int(callback_query.data.split('_')[1])
    options = ['Буду', 'Точно не знаю', 'Не смогу']
    selected_option = options[selected_option_index]
    await state.update_data(will_be=selected_option)
    await callback_query.message.answer("Если будешь +1, пиши +1, если есть другие комментарии, тоже пиши")
    await state.set_state(RegisterAccount.comment)


@router.message(RegisterAccount.comment, F.text)
async def add_comment(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    values = tuple(data for data in data.values())
    insert_account_query = f'insert into account (first_name, last_name, will_be, comment) values (%s, %s, %s, %s)'
    try:
        cur.execute(insert_account_query, values)
        conn.commit()
    except Exception as e:
        await message.answer("Нене, зарегистрироваться можно только 1 раз")
    else:
        await message.answer("Регистрация завершена, теперь можно посмотреть детали")



@router.message(Command(commands='members'))
async def get_members(message: types.Message):
    all_member_query = 'select first_name, last_name, will_be, comment from account'
    cur.execute(all_member_query)
    members = cur.fetchall()
    formatted_members = "\n".join([f"{member[0]} {member[1]}" for member in members])

    await message.answer(formatted_members)


@router.message(Command(commands="location"))
async def get_location(message: types.Message):
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
    )


@router.message(StateFilter(None), Command(commands="wishes"))
async def create_wish(message: types.Message, state: FSMContext):
    await message.answer("Если есть любые пожелания, пиши их здесь", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(CreateWish.wish)


@router.message(CreateWish.wish, F.text)
async def get_wish(message: types.Message, state: FSMContext):
    await state.update_data(comment=message.text)
    data = await state.get_data()
    if data:
        values = tuple(data for data in data.values())
        insert_account_query = f'insert into wish (wish) values (%s)'
        cur.execute(insert_account_query, values)
        conn.commit()
