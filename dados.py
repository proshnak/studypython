# This file contains the source code of AchicaynaBot a friendly and polite Telegram Bot.

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from auth import token2
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging
import asyncio
import random
from telegram.ext import CallbackQueryHandler
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('KirikiVBot')
author = "None"
puntuacion1 = 3
puntuacion2 = 3
puntuacion3 = 3
puntuacion4 = 3
puntuacion5 = 3
puntuacion6 = 3
dado1 = 0
dado2 = 0
#bot = telebot.TeleBot('835178478:AAG-77oqd-sD_q5IQ7q32zGwPWGGxncNHpE')

def quitarpunto(bot,update,args):

    if args[0] == '1':
        global puntuacion1
        puntuacion1 = puntuacion1 - 1
        logger.info(puntuacion1)
    elif args[0] == '2':
        global puntuacion2
        puntuacion2 = puntuacion2 - 1
    elif args[0] == '3':
        global puntuacion3
        puntuacion3 = puntuacion3 - 1
    elif args[0] == '4':
        global puntuacion4
        puntuacion4 = puntuacion4 - 1
    elif args[0] == '5':
        global puntuacion5
        puntuacion5 = puntuacion5 - 1
    elif args[0] == '6':
        global puntuacion6
        puntuacion6 = puntuacion6 - 1
    mostrarpuntos(bot,update)
    if puntuacion1 == 0:
        bot.send_message(
        chat_id=update.message.chat_id,
        text="Jugador 1 ha perdido."
    )
    elif puntuacion2 == 0:
        bot.send_message(
        chat_id=update.message.chat_id,
        text="Jugador 2 ha perdido."
    )
    elif puntuacion3 == 0:
        bot.send_message(
        chat_id=update.message.chat_id,
        text="Jugador 3 ha perdido."
    )
    elif puntuacion4 == 0:
        bot.send_message(
        chat_id=update.message.chat_id,
        text="Jugador 4 ha perdido."
    )
    elif puntuacion5 == 0:
        bot.send_message(
        chat_id=update.message.chat_id,
        text="Jugador 5 ha perdido."
    )
    elif puntuacion6 == 0:
        bot.send_message(
        chat_id=update.message.chat_id,
        text="Jugador 6 ha perdido."
    )
def mostrarpuntos(bot,update):
    global puntuacion1, puntuacion2, puntuacion3, puntuacion4, puntuacion5, puntuacion6
    logger.info('He recibido un comando mostrarpuntos')
    bot.send_message(
        chat_id=update.message.chat_id,
        text= "Jugador 1: "+str(puntuacion1)+"\nJugador 2: "+str(puntuacion2)+"\nJugador 3: "+str(puntuacion3)+"\nJugador 4: "+str(puntuacion4)+"\nJugador 5: "+str(puntuacion5)+"\nJugador 6: "+str(puntuacion6)
    )

def start(bot, update):
    logger.info('He recibido un comando start')
    bot.send_message(
        chat_id= update.message.chat_id,
        text="Bienvenid@ al juego del Kiriki."
    )
def tirardados(bot,update,args):
    global dado1, dado2
    dado1=random.randint(1,6)
    dado2=random.randint(1,6)
    if args[0] == "vela":
        bot.send_message(
            chat_id=518436603,
            text=str(dado1)+" - " + str(dado2)
        )
    if args[0] == "juanma":
        bot.send_message(
            chat_id=9113697,
            text=str(dado1)+" - " + str(dado2)
        )
    if args[0] == "toni":
        bot.send_message(
            chat_id=864451219,
            text=str(dado1)+" - " + str(dado2)
        )
def levantar(bot,update):
    global dado1, dado2
    bot.send_message(
        chat_id=update.message.chat_id,
        text=str(dado1)+" - " + str(dado2)
    )

if __name__ == '__main__':
    #dispatcher = updaterTelegram.dispatcher
    updaterTelegram = Updater(token = token2, request_kwargs={'read_timeout': 10, 'connect_timeout': 10})
    updaterTelegram.dispatcher.add_handler(CommandHandler('start', start))
    updaterTelegram.dispatcher.add_handler(CommandHandler('levantar', levantar))
    updaterTelegram.dispatcher.add_handler(CommandHandler('tirardados', tirardados, pass_args=True))
    updaterTelegram.dispatcher.add_handler(CommandHandler('quitarpunto', quitarpunto, pass_args=True))
    updaterTelegram.dispatcher.add_handler(CommandHandler('mostrarpuntos', mostrarpuntos))
    updaterTelegram.start_polling()
    updaterTelegram.idle()

