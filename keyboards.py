from aiogram import types as tp

keyboard_start = tp.InlineKeyboardMarkup(row_width=1)

start_buttons = [
    tp.InlineKeyboardButton(text='Get an anonymous message', callback_data='anonymous_message'),
    tp.InlineKeyboardButton(text='Help 🚩', callback_data='help'),
    tp.InlineKeyboardButton(text='Subscription 🕗', callback_data='donate'),

]
keyboard_start.add(*start_buttons)


keyboard_money_format = tp.InlineKeyboardMarkup(row_width=1)

money_format_buttons = [
    tp.InlineKeyboardButton(text='Cash rate 💳', callback_data='cash_rate'),
    tp.InlineKeyboardButton(text='Non-cash rate 💶', callback_data='non-cash_rate'),
    tp.InlineKeyboardButton(text='< Back -', callback_data='back')
]
keyboard_money_format.add(*money_format_buttons)