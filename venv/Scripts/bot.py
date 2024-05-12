import os
import telebot
import requests

from fpdf import FPDF
from PdfSetting import PdfSetting


with open('api', 'r') as f:
    BOT_TOKEN = f.readline()
    f.close()

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi, write /text_to_pdf if you wish to convert your \".txt\" file into a pdf.")

@bot.message_handler(commands=['text_to_pdf', 'text-to-pdf'])
def text_to_pdf_initial(message):
    bot.send_message(message.chat.id, "Send a \".txt\" file and it will be converted into pdf.")

@bot.message_handler(content_types=['document'])
def get_document(message):
    print(message)
    path = "../files/" + message.document.file_name
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    with open(path, 'wb') as new_file:
        new_file.write(downloaded_file)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=15)
    with open(path, 'r') as f:
        for x in f:
            pdf.cell(200, 10, txt=x, ln=1, align='C')
        f.close()
    pdf.output(f"..{path.split('.')[2]}.pdf")
    bot.send_message(message.chat.id, "Here is the converted file!")
    with open(f"..{path.split('.')[2]}.pdf", "rb") as res:
        bot.send_document(message.chat.id, res)
        res.close()


bot.infinity_polling()
