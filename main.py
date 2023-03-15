from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType
from aiogram.utils import executor
import logging
from aiogram import Bot
import bot_token
from aiogram import types as tp
import keyboards as kb
import bdfunk as bd
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(bot_token.get_token())
dp = Dispatcher(bot, storage=MemoryStorage())

db_emoji = bd.Data_base_emoje_token('Data_base_emoji_token.db')
db = bd.Data_base_user('Data_base_user.db')

PRICE = tp.LabeledPrice(label="Activation for 1 month", amount=5*100)

logging.basicConfig(level=logging.DEBUG)


class SendMessage(StatesGroup):
    write_message = State()


@dp.message_handler(commands='start')
async def start(message: tp.Message, state: FSMContext):

    if len(message.get_args()) > 0 and db.check_for_presence_in_the_list(message.get_args()):
        await message.answer(
            f'You have followed the link of user {db.get_username(message.get_args())}, '
            f'write an anonymous message below'
        )
        await state.update_data(recipient_id=message.get_args())
        await state.set_state(SendMessage.write_message)

    elif db.check_for_presence_in_the_list(message.from_user.id):
        await message.answer('Functional menu', reply_markup=kb.keyboard_start)
    else:
        db.add_guests(message.from_user.id, message.from_user.first_name)
        await message.answer_sticker(db_emoji.get_token('hello_bot'))
        await message.answer(
            'Hello, welcome to the bot for sending anonymous messages\n'
            'Below is the menu of my functions\nYou can call it with the /start method',
            reply_markup=kb.keyboard_start
        )


@dp.message_handler(state=SendMessage.write_message)
async def send_message(message: tp.Message, state: FSMContext):
    user_data = await state.get_data()
    await bot.send_message(user_data['recipient_id'], f'You have received an anonymous message: {message.text}')
    await message.answer("Message sent successfully", reply_markup=kb.keyboard_start)
    await state.finish()


@dp.callback_query_handler(text='anonymous_message')
async def anonymous_message(call: tp.CallbackQuery):
    await call.message.answer(
        "Below is a link to send anonymous messages, referred users will be able to leave it to you\n"
        f"https://t.me/UntitledMessageBot?start={call.from_user.id}"
    )


@dp.callback_query_handler(text='donate')
async def donate(call: tp.CallbackQuery):
    if bot_token.get_payment_token().split(':')[1] == 'TEST':
        await bot.send_message(call.message.chat.id, "Test payment, money will not be debited")

    await bot.send_invoice(
        call.message.chat.id,
        title="Bot subscription",
        description="Bot subscription activation for 1 month",
        provider_token=bot_token.get_payment_token(),
        currency="usd",
        photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
        photo_width=416,
        photo_height=234,
        photo_size=416,
        is_flexible=False,
        prices=[PRICE],
        start_parameter="one-month-subscription",
        payload="test-invoice-payload"
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def pre_checkout_query(pre_checkout_q: tp.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: tp.Message):
    print("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f"{k} = {v}")

    await bot.send_message(
        message.chat.id,
        f"Payment for the amount {message.successful_payment.total_amount // 100}"
        f" {message.successful_payment.currency} passed successfully")


@dp.message_handler(commands='help')
async def help_command(message: tp.Message):
    await message.answer('This bot is designed to send and receive anonymous messages.\n'
                              'Write \start to call the function dispatcher', reply_markup=kb.keyboard_start)


@dp.callback_query_handler(text='help')
async def help(call: tp.CallbackQuery):
    await call.message.answer('This bot is designed to send and receive anonymous messages.\n'
                              'Write \start to call the function dispatcher', reply_markup=kb.keyboard_start)

if __name__ == '__main__':
    executor.start_polling(dp)
