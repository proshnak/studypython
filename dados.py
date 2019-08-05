# This file contains the source code of AchicaynaBot a friendly and polite Telegram Bot.

from telegram.ext import Updater, CommandHandler
from auth import token2
import logging
import random
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('KirikiVBot')

#clase partida, que creará una partida.
#contiene el código de la partida, una lista de los jugadores, los dos dados, el turno en el que estamos y la última tirada

class partida:
    codigo = ''
    jugadores = []
    dado1 = 1
    dado2 = 1
    turno = 0
    ultimatirada = "verdad"
    #Método constructor de partida
    def __init__(self, cod, jug):
        self.codigo = cod
        self.jugadores = jug
        self.dado1 = 1
        self.dado2 = 1
        self.turno = 0
        self.ultimatirada = "verdad"
#Clase jugador, que define los atributos del mismo.
#Contiene el nombre del jugador, su id (idaso) y su puntuación
class jugador:
    nombre = ''
    idaso = ''
    puntos = 3
    #Método constructor de jugador
    def __init__(self, nombre, idaso):
        self.nombre = nombre
        self.idaso = idaso
        self.puntos = 3

#lista de partidas. Aquí se almacenarán todas las partidas
partidas = []

#método que creará una nueva partida si es posible
def crearpartida (bot,update):
    logger.info('He recibido un comando crearpartida')
    correcto = True
    #Creamos un bucle para que, en caso de que el código de la partida salga repetido, vuelva a generar otro.
    while correcto:
        bucle = 0
        #El código de la partida se genera creando 3 números aleatorios y concatenándolos como string (str)
        cod=str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
        #creamos un objeto partida. En caso de que sea una partida repetida, se machacará el mismo.
        jug = []
        partidanueva = partida(cod, jug)
        #Llamamos a la lista global de partida
        global partidas
        #con un bucle for each, recorremos la lista de partidas.
        if len(partidas)==0:
            partidas.append(partidanueva)
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Partida creada. Código_partida: " + cod
            )
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Jugadores, id uniendose con el comando (join nombre id codigo_partida)\n Podéis obtener vuestro id de este bot: https://web.telegram.org/#/im?p=@userinfobot "
            )
            correcto = False
        else:
            for i in range(len(partidas)):
                #Si el código nuevo coincide con uno existente, el bucle se repite.
                if cod==partidas[i].codigo:
                    bucle = bucle + 1
                    correcto = True
                    logger.info(bucle)
                    #Si el código se repite 50 veces o más (algo muy improbable), se dará por hecho que el cupo de partidas (1000) está completo, y hay que esperar a que se vacíe
                    if bucle>=50:
                        bot.send_message(
                        chat_id=update.message.chat_id,
                        text="Ups. La partida no ha podido ser creada. Es probable que los servidores estén llenos. Prueba de nuevo más tarde."
                        )
                        break
                else:
                    partidas.append(partidanueva)
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text="Partida creada. Código_partida: " + cod
                    )
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text="Jugadores, id uniendose con el comando (join nombre tu_id codigo_partida)\nPodéis obtener vuestro id de este bot: https://web.telegram.org/#/im?p=@userinfobot\nEjemplo de uso: join antonio 34124134 123 "
                    )
                    correcto = False

#Método mostrar partidas
def mostrarpartidas(bot,update):
    logger.info('He recibido un comando mostrarpartidas')
    global partidas
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Partidas disponibles: "
    )
    #Mientras el número de partidas no sea 0, el bucle recorrerá la lista y mostrará el código de cada partida.
    if len(partidas)!=0:
        for i in range(len(partidas)):
            bot.send_message(
                chat_id=update.message.chat_id,
                text=str(partidas[i].codigo)+"\n"
            )
#Método join, que unirá a los jugadores a la partida seleccionada
def join (bot,update,args):
    global partidas
    #Creamos el objeto pj con los argumentos recibidos
    pj = jugador(args[0], args[1])
    logger.info('He recibido un comando join')
    #Si no hay partidas, la partida no existe
    if len(partidas)==0:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="No existe ninguna partida con el código " + args[2]
        )
    else:
        anadido = 0
        #Recorremos la lista para comprobar que la partida existe y añadimos al jugador.
        for i in range(len(partidas)):
            if args[2]==partidas[i].codigo:
                partidas[i].jugadores.append(pj)
                bot.send_message(
                        chat_id=update.message.chat_id,
                        text="Jugador " + args[0] + " añadido a la partida " + args[2]+"\nPara tirar los dados usa el comando (tirardados nombre codigo_partida)\nEjemplo: tirardados antonio 123"
                    )
                anadido = 1
        #Si la partida no existe, avisamos al jugador
        if anadido == 0:
            bot.send_message(
                chat_id=update.message.chat_id,
                text="No existe ninguna partida con el código " + args[2]
            )

#Método para quitarle un punto a un jugador. Este método no será visible por el usuario.
def quitarpunto(partida,nombre):
    global partidas
    for i in range(len(partidas[partida].jugadores)):
        if nombre == partidas[partida].jugadores[i].nombre:
            partidas[partida].jugadores[i].puntos = partidas[partida].jugadores[i].puntos - 1

#Método para mostrar los puntos de la partida. Recibe como argumento el código de la partida
def mostrarpuntos(bot,update, args):
    global partidas
    logger.info('He recibido un comando mostrarpuntos')
    for i in range(len(partidas)):
        if args[0]==partidas[i].codigo:
            for e in range(len(partidas[i].jugadores)):
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text= partidas[i].jugadores[e].nombre+": "+str(partidas[i].jugadores[e].puntos)
                )

#Método de bienvenida
def start(bot, update):
    logger.info('He recibido un comando start')
    bot.send_message(
        chat_id= update.message.chat_id,
        text="Bienvenid@ al juego del Kiriki. Use el comando (crearpartida) para crear una nueva partida."
    )

#Método para tirar dados. Deberás indicar tu nombre y el número de la partida
def tirardados(bot,update,args):
    logger.info('He recibido un comando tirardados')
    global partidas
    for i in range(len(partidas)):
        if args[0]==partidas[i].codigo:
            partidas[i].dado1=random.randint(1,6)
            partidas[i].dado2=random.randint(1,6)
            for e in range(len(partidas[i].jugadores)):
                if e == partidas[i].turno:
                    #logger.info(partida[i].jugadores[e].idaso
                    if partidas[i].dado1 == 1:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('1.png', 'rb'))
                    elif partidas[i].dado1 == 2:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('2.png', 'rb'))
                    elif partidas[i].dado1 == 3:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('3.png', 'rb'))
                    elif partidas[i].dado1 == 4:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('4.png', 'rb'))
                    elif partidas[i].dado1 == 5:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('5.png', 'rb'))
                    elif partidas[i].dado1 == 6:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('6.png', 'rb'))

                    if partidas[i].dado2 == 1:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('1.png', 'rb'))
                    elif partidas[i].dado2 == 2:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('2.png', 'rb'))
                    elif partidas[i].dado2 == 3:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('3.png', 'rb'))
                    elif partidas[i].dado2 == 4:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('4.png', 'rb'))
                    elif partidas[i].dado2 == 5:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('5.png', 'rb'))
                    elif partidas[i].dado2 == 6:
                        bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('6.png', 'rb'))
                    logger.info(str(partidas[i].turno)+str(len(partidas[i].jugadores)-1))
                    if partidas[i].turno == len(partidas[i].jugadores)-1:
                        bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", dile lo que has sacado a "+partidas[i].jugadores[0].nombre + " por el grupo. ¿Mientes o dices la verdad?.")
                    else:
                        bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", dile lo que has sacado a "+partidas[i].jugadores[e+1].nombre + " por el grupo. ¿Mientes o dices la verdad?.")
                    #bot.send_message(
                    #    chat_id= update.message.chat_id,
                    #    text=partida[i].jugadores[e+1].nombre + ", "+partida[i].jugadores[e].nombre + " va a decirte lo que ha sacado por el grupo. Puedes levantar si crees que miente."
                    #)


def pasar(bot,update,args):
    for i in range(len(partidas)):
        if partidas[i].codigo == args[0]:
            if partidas[i].turno == len(partidas[i].jugadores)-1:
                partidas[i].turno = 0
                bot.send_message(
                        chat_id=update.message.chat_id,
                        text="Has pasado sin levantar. Te toca a ti."
                    )
            else:
                partidas[i].turno = partidas[i].turno+1
                bot.send_message(
                        chat_id=update.message.chat_id,
                        text="Has pasado sin levantar. Te toca a ti."
                    )

def verdad(bot,update,args):
    for i in range(len(partidas)):
        if partidas[i].codigo == args[0]:
            partidas[i].ultimatirada = "verdad"
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Has dicho la verdad."
            )
def mentira(bot,update,args):
    for i in range(len(partidas)):
        if partidas[i].codigo == args[0]:
            partidas[i].ultimatirada = "mentira"
            bot.send_message(
                chat_id=update.message.chat_id,
                text="Has mentido."
            )

def levantar(bot,update,args):
    for i in range(len(partidas)):
        if partidas[i].ultimatirada == "verdad":
            for e in range(len(partidas[i].jugadores)):
                if e == partidas[i].turno:

                    if partidas[i].turno == len(partidas[i].jugadores)-1:
                        partidas[i].jugadores[0].puntos = (partidas[i].jugadores[0].puntos)-1
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text="El jugador "+partidas[i].jugadores[0].nombre + " ha perdido un punto por levantar una verdad. Le queda: " + str(partidas[i].jugadores[0].puntos)
                        )
                        partidas[i].turno = 0
                    else:
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text="El jugador "+partidas[i].jugadores[e+1].nombre + " ha perdido un punto por levantar una verdad. Le queda: "+ str(partidas[i].jugadores[e+1].puntos)
                        )
                        partidas[i].turno = (partidas[i].turno)+1
                    if partidas[i].jugadores[e+1].puntos == 0:
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text="El jugador "+partidas[i].jugadores[e+1].nombre + " ha sido derrotado. Quedas eliminado."
                        )

                    del partidas[i].jugadores[e+1]
        else:
            for e in range(len(partidas[i].jugadores)):
                if e == partidas[i].turno:
                    partidas[i].jugadores[e].puntos = (partidas[i].jugadores[e].puntos)-1

                    if partidas[i].turno == len(partidas[i].jugadores)-1:
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text="El jugador "+partidas[i].jugadores[e].nombre + " ha perdido un punto por mentir. Le queda: "+ str(partidas[i].jugadores[e].puntos)
                        )
                        partidas[i].turno = 0
                    else:
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text="El jugador "+partidas[i].jugadores[0].nombre + " ha perdido un punto por mentir. Le queda: "+ str(partidas[i].jugadores[0].puntos)
                        )
                        partidas[i].turno = (partidas[i].turno)+1
                    if partidas[i].jugadores[e].puntos == 0:
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text="El jugador "+partidas[i].jugadores[e].nombre + " ha sido derrotado. Quedas eliminado."
                        )
                        del partidas[i].jugadores[e]

def mispartidas(bot,update,args):
    bot.send_message(chat_id=update.message.chat_id, text=args[0]+", estás jugando en las siguientes partidas: \n.")
    for i in range(len(partidas)):
        for e in range(len(partidas[i].jugadores)):
            if partidas[i].jugadores[e].nombre == args[0]:
                bot.send_message(chat_id=update.message.chat_id, text=partidas[i].codigo+"\n.")

if __name__ == '__main__':
    #dispatcher = updaterTelegram.dispatcher
    updaterTelegram = Updater(token = token2, request_kwargs={'read_timeout': 10, 'connect_timeout': 10})
    updaterTelegram.dispatcher.add_handler(CommandHandler('start', start))
    updaterTelegram.dispatcher.add_handler(CommandHandler('levantar', levantar, pass_args=True))
    updaterTelegram.dispatcher.add_handler(CommandHandler('tirardados', tirardados, pass_args=True))
    updaterTelegram.dispatcher.add_handler(CommandHandler('mostrarpuntos', mostrarpuntos, pass_args=True))
    updaterTelegram.dispatcher.add_handler(CommandHandler('crearpartida', crearpartida))
    updaterTelegram.dispatcher.add_handler(CommandHandler('join', join, pass_args=True))
    updaterTelegram.dispatcher.add_handler(CommandHandler('mostrarpartidas', mostrarpartidas))
    updaterTelegram.dispatcher.add_handler(CommandHandler('mispartidas', mispartidas, pass_args=True))
    updaterTelegram.dispatcher.add_handler(CommandHandler('verdad', verdad, pass_args=True))
    updaterTelegram.dispatcher.add_handler(CommandHandler('mentira', mentira, pass_args=True))
    updaterTelegram.dispatcher.add_handler(CommandHandler('pasar', pasar, pass_args=True))
    updaterTelegram.start_polling()
    updaterTelegram.idle()