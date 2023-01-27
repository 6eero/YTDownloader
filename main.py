"""
A Python script to download YouTube audio
trougth a telegram bot
"""

from pytube import YouTube
import os

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from datetime import datetime



def start(update: Update, context: CallbackContext):
    update.message.reply_text("Benvenuto/a nel mio bot per scaricare musica da YouTube")
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)

def yt_downloader(link):

    yt = YouTube(link)
    stream = yt.streams.filter(only_audio=True).first()
    out_file = stream.download()
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

def scarica_e_invia(update: Update, context: CallbackContext):

    link = update.message.text[8:]
    yt_downloader(link)

    with open('downloadedlogs.txt', 'a') as file:
        file.write(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + " Downloaded: " + link)

    for item in os.listdir(dir_name):
        if item.endswith(".mp3"):
            song_name = dir_name + item

    context.bot.send_audio(chat_id=update.message.chat_id, audio=open(song_name, 'rb'), timeout=360)

    for item in os.listdir(dir_name):
        if item.endswith(".mp3"):
            os.remove(os.path.join(dir_name, item))


if __name__ == "__main__":

    dir_name = '/Users/Gerot/Documents/PythonProjects/YTDownloader/'

    with open('/Users/Gerot/Desktop/key.txt', 'r') as file:
        key = file.read().rstrip()

    updater = Updater(key, use_context=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('scarica', scarica_e_invia))
    updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    updater.start_polling()



