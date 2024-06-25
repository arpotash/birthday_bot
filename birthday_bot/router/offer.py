from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import types
from aiogram.fsm.context import FSMContext

from db import cur, conn
from aiogram.fsm.state import State, StatesGroup

offer_router = Router()


class CreateWish(StatesGroup):
    wish = State()



@offer_router.message(Command(commands='members'))
async def get_members(message: types.Message):
    all_member_query = 'select first_name, last_name, will_be, comment from account'
    cur.execute(all_member_query)
    members = cur.fetchall()
    formatted_members = "\n".join([f"{member[0]} {member[1]} {member[2]}" for member in members])
    await message.answer(formatted_members)


@offer_router.message(Command(commands="location"))
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

# @offer_router.message(StateFilter(None), Command(commands="wishes"))
# async def create_wish(message: types.Message, state: FSMContext):
#     await message.answer("Если есть любые пожелания, пиши их здесь", reply_markup=types.ReplyKeyboardRemove())
#     await state.set_state(CreateWish.wish)

#
# @offer_router.message(CreateWish.wish, F.text)
# async def get_wish(message: types.Message, state: FSMContext):
#     await state.update_data(comment=message.text)
#     data = await state.get_data()
#     if data:
#         values = tuple(data for data in data.values())
#         insert_account_query = f'insert into wish (wish) values (%s)'
#         try:
#             cur.execute(insert_account_query, values)
#             conn.commit()
#             await message.answer("Пожелания учтены, спасибо!")
#         except Exception as e:
#             await message.answer("Упс, кажется, сервак упал")
#             conn.rollback()
#             raise e
#         finally:
#             await state.clear()
