import logging
import pandas as pd
import telegram
import numpy as np
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import requests


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
bot = telegram.Bot(token='5567475614:AAHCNydq4QLcJlHfCPvWVwUfEHviguIKJi8')
try:
    chat_id = bot.get_updates()[-1].message.chat_id
except IndexError:
    chat_id = 0
####################################################################################################################


def itr():
    return iter(["Costo KW/h ( 1 cent = 0.01 )", "Cantidad de TH",
                 "Consumo en Kwatts  (1,000 Watss = 1 Kwatss)"])


def blockchain_stats():
    # Info Blockchain Stats
    url_pool = "https://api.blockchain.info/stats"
    r = requests.get(url_pool)
    return r.json()


class data:
    iterList = itr()
    const = []
    x = ''
    stat = blockchain_stats()


def calcProfit(kW, Th, consuptionW):
    # por el momento que lo pida cada vez que se pida luego lo hacemos con un pool.
    profit = Th*ThConstProfit()*data.stat['market_price_usd']
    lightCost = kW*24*consuptionW
    result = profit - lightCost
    return result


def ThConstProfit():
    # For now is only Statit Calc but should be more efficient
    binance_calc = 0.00012648 / 37.14
    return binance_calc


def soporte(update, context):

    update.message.reply_text('''Hola!, Soy un Bot Beta que calcula el Profit Diario y Mensual basado en el consumo KW/h y El poder de Computo en (TH). Por ahora me crearon con ese fin quizas con el tiempo de uso podre desarrollar mas herramientas y mas facil para ti. Esto es un desarrollo de Doctorminer & Leviatan CryptoLab.
    Los Creadores de este Proyecto: Juan Vicente Ventrone y Theo Toukoumidis.\n Nota!: Es un desarrollo Beta puede tener Fallas.
    https://t.me/JVentrone''')


def resultCalc(update, context):
    keyboard = [[InlineKeyboardButton(
        " ⚡ DE NUEVO ⚡ ", callback_data='getVariables'), ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    try:
        costKw = float(data.const[0])
        Th = float(data.const[1])
        consuptionW = float(data.const[2])
        data.const = []
        value = round(calcProfit(costKw, Th, consuptionW), 4)
        valueMonth = value*30
        update.message.reply_text('Profit Diario: $' + str(value) + '\n'
                                  'Profit Mensual: $' + str(valueMonth), reply_markup=reply_markup
                                  )
    except:
        update.message.reply_text(
            'Ups😵, Debes ingresar un valor valido, es decir solo numeros!', reply_markup=reply_markup)


def start(update, context: CallbackContext):
    keyboard = [[InlineKeyboardButton(
        " ⚡ EMPEZAR ⚡ ", callback_data='getVariables'), ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        'Hola! ' + str(update.message.chat.username) +
        ', Para Calcular el Profit Diario y Mensual necesito saber coste en costKw/h, el Hashrate (Poder de Computo) en TH y el consumo electrico en Kwatts.\n' +
        'Mayor Informacion de este Bot /info\n' +
        '¿Quienes somos? /soporte', reply_markup=reply_markup
    )


def getVariables(update, context: CallbackContext):
    data.const = []
    data.stat = blockchain_stats()
    data.x = next(data.iterList)
    update.callback_query.message.reply_text(data.x)


def info(update, context):
    keyboard = [[InlineKeyboardButton(
        " ⚡EMPEZAR ⚡ ", callback_data='getVariables'), ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        'Resultado Diario: La recompensa Generada Diaria por su de poder de computo "Menos" El gasto del consumo electrico diario \n\n' +
        'Resultado Mensual: La recompensa Generada Mensual (30 Dias) por su poder de computo "Menos" El gasto del consumo electrico Mensual (30 Dias) \n', reply_markup=reply_markup
    )


def echo(update, context):
    data.const.append(update.message.text)

    if data.x == 'Consumo en Kwatts  (1,000 Watss = 1 Kwatss)':
        data.iterList = itr()
        resultCalc(update, context)
        return True
    data.x = next(data.iterList)
    update.message.reply_text(data.x)


def sticker(bot, update):
    reply = update.message.sticker.file_id
    bot.send_sticker(chat_id=update.message.chat_id, sticker=reply)


def main():

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        '5567475614:AAHCNydq4QLcJlHfCPvWVwUfEHviguIKJi8', use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    # p.add_handler(CommandHandler("menu", menu))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("calc", resultCalc))
    dp.add_handler(CommandHandler("soporte", soporte))
    dp.add_handler(CommandHandler("info", info))

    dp.add_handler(CallbackQueryHandler(
        getVariables, pattern='^getVariables$'))

    dp.add_handler(MessageHandler(Filters.sticker, sticker))
    dp.add_handler(MessageHandler(Filters.text, echo))
    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
