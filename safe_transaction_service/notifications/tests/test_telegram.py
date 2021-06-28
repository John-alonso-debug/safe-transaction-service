import pytest
import warnings
import telebot

TOKEN = 'input-bot-api-token-here'
chat_id = 'input-your-user'

#
#
#
bot = telebot.TeleBot(TOKEN)
tb = telebot.TeleBot(TOKEN)  # create a new Telegram Bot object


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


# bot.polling()
# tb.polling(none_stop=False, interval=0, timeout=20)


# sendMessage
# tb.send_message(chat_id, text)

#
def test_telegram():
    # getMe
    me = tb.get_me()
    print('bot info:', me)

    # tb.send_message(chat_id=chat_id, text='hello from bot')

    # get bot cmds:
    cmds = tb.get_my_commands()

    tb.inline_handler()

    for item in cmds:
        print('bot cmd: ', item)

    # tb.set_my_commands()
    # tb.send_message(chat_id, text)

    # del webhook:
    # tb.delete_webhook()

    msg = tb.get_updates()

    for item in msg:
        print('bot msg: ', item)
