# Este código está muy en bruto. Será necesario editarlo para que cada clase esté en su fichero correspondiente, haciendo así el código más legible

#Versión actual ESTABLE 0.6.0

#Importamos las clases correspondientes. También importamos el archivo auth.py, que es donde está la autenticación de mis bots
#from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from auth import token2
import logging
import random
from telegram.ext import CallbackQueryHandler
#import pickle
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('KirikiVBot')
FIRST, SECOND, THIRD = range(3)
#clase partida, que creará una partida.
#contiene el código de la partida, una lista de los jugadores, los dos dados, el turno en el que estamos y la última tirada

class partida:
    codigo = ''
    jugadores = []
    #los dados pueden llegar a sobrar, estoy por quitarlos
    dado1 = 1
    dado2 = 1
    turno = 0
    ultimatirada = 0
    id_chat = ''
    respuesta = 0
    #Método constructor de partida
    def __init__(self, cod, jug, chat_id):
        self.codigo = cod
        self.jugadores = jug
        self.dado1 = 1
        self.dado2 = 1
        self.turno = 0
        self.ultimatirada = 0
        self.id_chat = chat_id
        self.respuesta = 0
#Clase jugador, que define los atributos del mismo.
#Contiene el nombre del jugador, su id (idaso) y su puntuación
class jugador:
    nombre = ''
    idaso = ''
    puntos = 3
    actualpartida = 0
    #Método constructor de jugador
    def __init__(self, nombre, idaso):
        self.nombre = nombre
        self.idaso = idaso
        self.puntos = 3
        self.actualpartida = 0

#lista de partidas. Aquí se almacenarán todas las partidas
partidas = []

#método que creará una nueva partida si es posible
def crearpartida (bot,update):
    #cargar(bot,update)
    logger.info('He recibido un comando crearpartida')
    correcto = True
    #Creamos un bucle para que, en caso de que el código de la partida salga repetido, vuelva a generar otro.
    while correcto:
        bucle = 0
        #El código de la partida se genera creando 3 números aleatorios y concatenándolos como string (str)
        cod=str(random.randint(0,9))+str(random.randint(0,9))+str(random.randint(0,9))
        #creamos un objeto partida. En caso de que sea una partida repetida, se machacará el mismo.
        jug = []
        partidanueva = partida(cod, jug, update.message.chat_id)
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
                text="Jugadores, id uniendose con el comando (join codigo_partida)\n"
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
                    correcto = False

def jugadorexiste(bot,update,partida):
    global partidas
    for i in range(len(partidas)):
        if partidas[i].codigo == partida:
            if len(partidas[i].jugadores) == 0:
                resultado = False
                return resultado
                break
            else:
                for e in range(len(partidas[i].jugadores)):
                    if partidas[i].jugadores[e].idaso == update.message.from_user.id:
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text="Ya estabas unido a esa partida con anterioridad."
                        )
                        resultado = True
                        return resultado
                        break
                    resultado = False
                    return resultado
                    break


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
    #Creamos el objeto pj con el argumento update
    pj = jugador(update.message.from_user.first_name, update.message.from_user.id)
    logger.info('He recibido un comando join')
    #Si no hay partidas, la partida no existe
    if len(partidas)==0:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="No existe ninguna partida con el código " + args[0]
        )
    else:
        anadido = 0
        #Recorremos la lista para comprobar que la partida existe y añadimos al jugador.
        for i in range(len(partidas)):
            if args[0]==partidas[i].codigo:
                existe = jugadorexiste(bot,update,args[0])
                if (existe == False):
                    logger.info('Jugador existe devuelve false.')
                    partidas[i].jugadores.append(pj)
                    bot.send_message(
                            chat_id=update.message.chat_id,
                            text="Jugador " + update.message.from_user.first_name + " añadido a la partida " + args[0]+"\nPara tirar los dados usa el comando /tirardados. (Si no es tu turno, el juego te avisará)."
                        )
                    for e in range (len(partidas[i].jugadores)):
                        if partidas[i].jugadores[e].idaso == update.message.from_user.id:
                            partidas[i].jugadores[e].actualpartida = args[0]
                    anadido = 1
                    break
                else:
                    anadido = 1
        #Si la partida no existe, avisamos al jugador
        if anadido == 0:
            bot.send_message(
               chat_id=update.message.chat_id,
               text="No existe ninguna partida con el código " + args[0]
           )

#Método para quitarle un punto a un jugador. Este método no será visible por el usuario.
def quitarpunto(partida,nombre):
    global partidas
    for i in range(len(partidas[partida].jugadores)):
        if nombre == partidas[partida].jugadores[i].nombre:
            partidas[partida].jugadores[i].puntos = partidas[partida].jugadores[i].puntos - 1

#Método para mostrar los puntos de la partida. Recibe como argumento el código de la partida
def mostrarpuntos(bot,update):
    global partidas
    logger.info('He recibido un comando mostrarpuntos')
    for i in range(len(partidas)):
        for e in range (len(partidas[i].jugadores)):
            if partidas[i].jugadores[e].actualpartida == partidas[i].codigo:
                for e in range(len(partidas[i].jugadores)):
                    bot.send_message(
                        chat_id=update.message.chat_id,
                        text= partidas[i].jugadores[e].nombre+": "+str(partidas[i].jugadores[e].puntos)
                    )
                break
#Método de bienvenida
def start(bot, update):
    logger.info('He recibido un comando start')
    bot.send_message(
        chat_id= update.message.chat_id,
        text="Bienvenid@ al juego del Kiriki. Use el comando /ayuda para que sepas como jugar."
    )

#Método para tirar dados. Deberás indicar tu nombre y el número de la partida
def tirardados(bot,update):
    logger.info('He recibido un comando tirardados')
    global partidas
    tiradabuena = 0
    for i in range(len(partidas)):
        if update.message.chat_id == partidas[i].id_chat:
            for e in range(len(partidas[i].jugadores)):
                if partidas[i].jugadores[e].idaso == update.message.from_user.id:
                    if e == partidas[i].turno:
                        dado1=random.randint(1,6)
                        dado2=random.randint(1,6)
                        #logger.info(partida[i].jugadores[e].idaso Esto está aquí para descomentarlo por si el código da fallo, para verlo en la terminal.
                        if dado1 == 1:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('1.png', 'rb'))
                        elif dado1 == 2:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('2.png', 'rb'))
                        elif dado1 == 3:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('3.png', 'rb'))
                        elif dado1 == 4:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('4.png', 'rb'))
                        elif dado1 == 5:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('5.png', 'rb'))
                        elif dado1 == 6:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('6.png', 'rb'))

                        if dado2 == 1:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('1.png', 'rb'))
                        elif dado2 == 2:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('2.png', 'rb'))
                        elif dado2 == 3:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('3.png', 'rb'))
                        elif dado2 == 4:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('4.png', 'rb'))
                        elif dado2 == 5:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('5.png', 'rb'))
                        elif dado2 == 6:
                            bot.send_sticker(chat_id=partidas[i].jugadores[e].idaso, sticker=open('6.png', 'rb'))
                        tirada = dado1 + dado2
                        if dado1 == dado2:
                            partidas[i].ultimatirada = 12
                            bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", has sacado PAREJA")
                        elif tirada == 3:
                            bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", has sacado KIRIKI. Tú ganas.")
                            partidas[i].ultimatirada = 13
                            if len(partidas[i].jugadores) == partidas[i].turno+1:
                                bot.send_message(chat_id=update.message.chat_id, text= "El jugador "+partidas[i].jugadores[0].nombre+" ha perdido un punto por KIRIKI. Te toca tirar.")
                                partidas[i].jugadores[0].puntos = partidas[i].jugadores[0].puntos - 1
                                if partidas[i].jugadores[0].puntos == 0:
                                    bot.send_message(
                                        chat_id=update.message.chat_id,
                                        text= partidas[i].jugadores[0].nombre + " ha perdido."
                                    )
                                    partidas[i].jugadores.pop(0)
                                partidas[i].turno = 0
                                break
                            else:
                                bot.send_message(chat_id=update.message.chat_id, text= "El jugador "+partidas[i].jugadores[e+1].nombre+" ha perdido un punto por KIRIKI. Te toca tirar.")
                                partidas[i].jugadores[e+1].puntos = partidas[i].jugadores[e+1].puntos - 1
                                if partidas[i].jugadores[e+1].puntos == 0:
                                    bot.send_message(
                                        chat_id=update.message.chat_id,
                                        text= partidas[i].jugadores[e+1].nombre + " ha perdido."
                                    )
                                    partidas[i].jugadores.pop(e+1)
                                partidas[i].turno = partidas[i].turno + 1
                                break
                        elif tirada == 4:
                            bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", has sacado un 4.")
                            partidas[i].ultimatirada = 4
                        elif tirada == 5:
                            bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", has sacado un 5.")
                            partidas[i].ultimatirada = 5
                        elif tirada == 6:
                            bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", has sacado un 6.")
                            partidas[i].ultimatirada = 6
                        elif tirada == 7:
                            bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", has sacado un 7.")
                            partidas[i].ultimatirada = 7
                        elif tirada == 8:
                            bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", has sacado un 8.")
                            partidas[i].ultimatirada = 8
                        elif tirada == 9:
                            bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", has sacado un 9.")
                            partidas[i].ultimatirada = 9
                        elif tirada == 10:
                            bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", has sacado un 10.")
                            partidas[i].ultimatirada = 10
                        elif tirada == 11:
                            bot.send_message(chat_id=partidas[i].jugadores[e].idaso, text=partidas[i].jugadores[e].nombre + ", has sacado LADRILLO.")
                            partidas[i].ultimatirada = 11
                        tiradabuena == 1
                        logger.info(str(partidas[i].turno)+str(len(partidas[i].jugadores)-1))
                        keyboard = [[InlineKeyboardButton("Pareja", callback_data='9'), InlineKeyboardButton("Ladrillo", callback_data='8'), InlineKeyboardButton("10", callback_data='7')],
                        [InlineKeyboardButton("9", callback_data='6'), InlineKeyboardButton("8", callback_data='5'), InlineKeyboardButton("7", callback_data='4')],
                        [InlineKeyboardButton("6", callback_data='3'), InlineKeyboardButton("5", callback_data='2'), InlineKeyboardButton("4", callback_data='1')], ]
                        reply_markup=InlineKeyboardMarkup(keyboard, one_time_keyboard=True)
                        bot.send_message(chat_id=update.message.chat_id, text='Selecciona lo que has sacado o MIENTE si es necesario.', reply_markup=reply_markup)
        break
def tirardados2(bot,update):
    global partidas
    print('tuputamadre')
    for i in range (len(partidas)):
        for e in range (len(partidas[i].jugadores)):
            if partidas[i].jugadores[e].idaso == update.callback_query.from_user.id and partidas[i].codigo == partidas[i].jugadores[e].actualpartida:
                query = update.callback_query
                logger.info('TELEGRAM query data: "%s" type: "%s"' % (
                    str(query.data), str(type(query.data))))
                if query.data == '1':
                    partidas[i].respuesta = 4
                    print("entrada\n")
                elif query.data == '2':
                    partidas[i].respuesta = 5
                    print("entrada el fallo\n")
                elif query.data == '3':
                    partidas[i].respuesta = 6
                    print("entrada\n")
                elif query.data == '4':
                    partidas[i].respuesta = 7
                    print("entrada\n")
                elif query.data == '5':
                    partidas[i].respuesta = 8
                    print("entrada\n")
                elif query.data == '6':
                    partidas[i].respuesta = 9
                    print("entrada\n")
                elif query.data == '7':
                    partidas[i].respuesta = 10
                    print("entrada\n")
                elif query.data == '8':
                    partidas[i].respuesta = 11
                    print("entrada\n")
                    if  len(partidas[i].jugadores) == partidas[i].turno+1:
                        bot.edit_message_text(text='Seleccion realizada. '+partidas[i].jugadores[e].nombre+" dice que ha sacado un LADRILLO. "+partidas[i].jugadores[0].nombre+", te toca /levantar o /tirardados para pasar.",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
                        partidas[i].turno = 0
                    else:
                        bot.edit_message_text(text='Seleccion realizada. '+partidas[i].jugadores[e].nombre+" dice que ha sacado un LADRILLO. "+partidas[i].jugadores[e+1].nombre+", te toca /levantar o /tirardados para pasar.",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
                        partidas[i].turno = partidas[i].turno + 1
                elif query.data == '9':
                    partidas[i].respuesta = 12
                    if  len(partidas[i].jugadores) == partidas[i].turno+1:
                        bot.edit_message_text(text='Seleccion realizada. '+partidas[i].jugadores[e].nombre+" dice que ha sacado PAREJA. "+partidas[i].jugadores[0].nombre+", te toca /levantar o /tirardados para pasar.",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
                        partidas[i].turno = 0
                    else:
                        bot.edit_message_text(text='Seleccion realizada. '+partidas[i].jugadores[e].nombre+" dice que ha sacado PAREJA. "+partidas[i].jugadores[e+1].nombre+", te toca /levantar o /tirardados para pasar.",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
                        partidas[i].turno = partidas[i].turno + 1
                if partidas[i].respuesta < 11:
                    if  len(partidas[i].jugadores) == partidas[i].turno+1:
                        bot.edit_message_text(text='Seleccion realizada. '+partidas[i].jugadores[e].nombre+" dice que ha sacado un "+str(partidas[i].respuesta)+". "+partidas[i].jugadores[0].nombre+", te toca /levantar o /tirardados para pasar.",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
                        partidas[i].turno = 0
                    else:
                        bot.edit_message_text(text='Seleccion realizada. '+partidas[i].jugadores[e].nombre+" dice que ha sacado un "+str(partidas[i].respuesta)+". "+partidas[i].jugadores[e+1].nombre+", te toca /levantar o /tirardados para pasar.",
                        chat_id=query.message.chat_id,
                        message_id=query.message.message_id)
                        partidas[i].turno = partidas[i].turno + 1

                ##Aquí se debe llamar al método de jugada


#Esto era levantar o pasar con teclado, pero por problemas técnicos no he podido hacerlo.

'''
def jugada(bot,update):
    query = update.callback_query
    keyboard2 = [[InlineKeyboardButton("/levantar", callback_data='15')],
                                [InlineKeyboardButton("/pasar", callback_data='16')]]
    reply_markup=InlineKeyboardMarkup(keyboard2, one_time_keyboard=True)
    bot.send_message(chat_id=query.message.chat_id, text='¿Levantas o pasas?', reply_markup=reply_markup)


def jugada2(bot,update):
    global partidas
    print('jugadad2')
    for i in range (len(partidas)):
        for e in range (len(partidas[i].jugadores)):
            if partidas[i].jugadores[e].idaso == update.message.from_user.id and partidas[i].codigo == partidas[i].jugadores[e].actualpartida:
                query = update.callback_query
                logger.info('TELEGRAM query data: "%s" type: "%s"' % (
                    str(query.data), str(type(query.data))))
                if query.data == '15':
                    bot.edit_message_text(text='Levantando.',
                chat_id=query.message.chat_id,
                message_id=query.message.message_id)
                    levantar(bot,update)
                elif query.data == '16':
                    bot.edit_message_text(text='Pasando.',
                chat_id=query.message.chat_id,
                message_id=query.message.message_id)
                    pasar(bot,update)


#Comando pasar. Pasa el turno sin que ocurra nada.
def pasar(bot,update):
    logger.info('He recibido un comando pasar')
    for i in range(len(partidas)):
        if partidas[i].codigo == args[0]:
            if partidas[i].turno == len(partidas[i].jugadores)-1:
                partidas[i].turno = 0
                bot.send_message(
                        chat_id=update.message.chat_id,
                        text="Has pasado sin levantar. Te toca a ti. Usa el comando tirardados"
                    )
            else:
                partidas[i].turno = partidas[i].turno+1
                bot.send_message(
                        chat_id=update.message.chat_id,
                        text="Has pasado sin levantar. Te toca a ti. Usa el comando tirardados"
                    )
'''

#Comando levantar. Levanta la última tirada, comprueba la misma en el objeto partida y detecta si es mentira o verdad, quitando el punto correspondiente.
#Este método es un cacao. Consecuencias de que no tener el switch en python :D
def levantar(bot,update):
    logger.info('He recibido un comando levantar')
    for i in range(len(partidas)):
        for e in range(len(partidas[i].jugadores)):
            if partidas[i].jugadores[e].idaso == update.message.from_user.id and partidas[i].turno == e:
                #por si el jugador es el último en jugar
                if partidas[i].turno == len(partidas[i].jugadores):
                    if partidas[i].ultimatirada == partidas[i].respuesta:
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text="Has levantado una verdad. Pierdes un punto, " + partidas[i].jugadores[0].nombre
                        )
                        partidas[i].jugadores[e].puntos = partidas[i].jugadores[0].puntos - 1
                        if partidas[i].jugadores[0].puntos == 0:
                            bot.send_message(
                                chat_id=update.message.chat_id,
                                text= partidas[i].jugadores[0].nombre + " ha perdido."
                            )
                            partidas[i].jugadores.pop(0)
                    else:
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text="Has levantado una mentira. " + partidas[i].jugadores[e].nombre + " pierde un punto"
                        )
                        partidas[i].jugadores[e].puntos = partidas[i].jugadores[e].puntos - 1
                        if partidas[i].jugadores[e].puntos == 0:
                            bot.send_message(
                                chat_id=update.message.chat_id,
                                text= partidas[i].jugadores[0].nombre + " ha perdido."
                            )
                            partidas[i].jugadores.pop(0)
                else:
                    if partidas[i].ultimatirada == partidas[i].respuesta:
                        bot.send_message(
                                chat_id=update.message.chat_id,
                                text="Has levantado una verdad. Pierdes un punto, " + partidas[i].jugadores[e].nombre
                            )
                        partidas[i].jugadores[e].puntos = partidas[i].jugadores[e].puntos - 1
                        if partidas[i].jugadores[e].puntos == 0:
                            bot.send_message(
                                chat_id=update.message.chat_id,
                                text= partidas[i].jugadores[e].nombre + " ha perdido."
                            )
                            partidas[i].jugadores.pop(e)
                    else:
                        bot.send_message(
                            chat_id=update.message.chat_id,
                            text="Has levantado una mentira. " + partidas[i].jugadores[e-1].nombre + " pierde un punto"
                        )
                        partidas[i].jugadores[e-1].puntos = partidas[i].jugadores[e-1].puntos - 1
                        if partidas[i].jugadores[e-1].puntos == 0:
                            bot.send_message(
                                chat_id=update.message.chat_id,
                                text= partidas[i].jugadores[e-1].nombre + " ha perdido."
                            )
                            partidas[i].jugadores.pop(e-1)


#Este comando está en desuso. Hay que editarlo para que pille el solo el id y diga en cuantas partidas está el jugador. Recomendable no probar
def mispartidas(bot,update,args):
    bot.send_message(chat_id=update.message.chat_id, text=args[0]+", estás jugando en las siguientes partidas: \n.")
    for i in range(len(partidas)):
        for e in range(len(partidas[i].jugadores)):
            if partidas[i].jugadores[e].nombre == args[0]:
                bot.send_message(chat_id=update.message.chat_id, text=partidas[i].codigo+"\n.")
def ayuda(bot,update):
    bot.send_message(chat_id=update.message.chat_id, text="PASOS PARA JUGAR: \n1: Crea una partida con /crearpartida\n2: Id uniéndose con /join codigo_partida\n3: Cuando estéis todos, que el primero en unirse use el comando /tirardados\n4: El siguiente jugador, si se cree la tirada, volverá a /tirardados . Si piensa que es mentira, usará /levantar")
    bot.send_message(chat_id=update.message.chat_id, text="Comandos extra:\n /mostrarpuntos - Muestra la puntuación de los que están jugando.\n /valores - Pequeña guía de los dados")


def valores(bot,update):
    bot.send_photo(chat_id=update.message.chat_id, photo=open('valores.png', 'rb'))

#Método main. Hace cosas. Dejémoslo ahí.
if __name__ == '__main__':
    #dispatcher = updaterTelegram.dispatcher No sé que pollas es esto, pero si está aquí, aunque esté comentado, aquí se queda.
    updaterTelegram = Updater(token = token2, request_kwargs={'read_timeout': 10, 'connect_timeout': 10})
    updaterTelegram.dispatcher.add_handler(CommandHandler('start', start))
    updaterTelegram.dispatcher.add_handler(CommandHandler('tirardados', tirardados))

    updaterTelegram.dispatcher.add_handler(CommandHandler('mostrarpuntos', mostrarpuntos))
    #updaterTelegram.dispatcher.add_handler(CommandHandler('jugada', jugada))
    '''
    Tiene que haber algún fallo por aquí, porque cuando entramos en jugada, este carga el callbackquery de los dados.
    Investigar para la versión 0.7.0 si es posible
    '''
    updaterTelegram.dispatcher.add_handler(CommandHandler('valores', valores))
    updaterTelegram.dispatcher.add_handler(CommandHandler('crearpartida', crearpartida))
    updaterTelegram.dispatcher.add_handler(CommandHandler('join', join, pass_args=True))
    updaterTelegram.dispatcher.add_handler(CommandHandler('mostrarpartidas', mostrarpartidas))
    updaterTelegram.dispatcher.add_handler(CommandHandler('mispartidas', mispartidas, pass_args=True))
    #updaterTelegram.dispatcher.add_handler(CommandHandler('pasar', pasar, pass_args=True))
    updaterTelegram.dispatcher.add_handler(CommandHandler('levantar', levantar))
    updaterTelegram.dispatcher.add_handler(CommandHandler('ayuda', ayuda))
    #updaterTelegram.dispatcher.add_handler(CallbackQueryHandler(jugada2, pattern='jugada'))
    updaterTelegram.dispatcher.add_handler(CallbackQueryHandler(tirardados2))


    updaterTelegram.start_polling(allowed_updates=[])
    updaterTelegram.idle()