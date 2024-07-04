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
