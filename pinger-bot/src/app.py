# -*- coding: utf-8 -*-

# Python
import logging
import requests
import schedule
import time
from os import getenv
from telegram.ext import Updater, CommandHandler

# App

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


TOKEN = getenv("TELEGRAM-BOT-TOKEN")
ROOM_ID = getenv("TELEGRAM-CHAT-ID")
CHECK_IPS_INTERVAL = getenv("CHECK-IPS-INVERVAL")

def get_ip_list():
    ip_list = []
    with open("ip_list.txt", 'r') as ip_list_file:
        for ip in ip_list_file.readlines():
            ip = ip.replace('\n', '')
            ip_list.append(ip)
    return ip_list

def check_ip_address_status():
    ip_status = []
    with open("ip_list.txt", 'r') as ip_list_file:
        for ip in ip_list_file.readlines():
            ip = ip.replace('\n', '')
            # Realiza una solicitud HTTP a la API REST y obtén la respuesta en formato JSON
            response = requests.get('http://pinger-svc:8000/api/v1/ip/check', params={"ip":ip})
            response = response.json()
            if not response['status']:
                ip_status.append(
                    {
                        "ip": ip,
                        "status": response['status']
                    }
                )
    return ip_status

def report_ip_address_status():
    # Obtiene la información de la API REST
    info = check_ip_address_status()
    message = ""
    for item in info:
        message += f"🛑🛑🛑 [ DOWN ] {item['ip']} no responde!!!\n"
        send_message(message)

def add_ip(update, context):
    ip = context.args[0]
    with open("ip_list.txt", 'a+') as ip_list_file:
        ip_list_file.write(ip + "\n")
    print(f'Se ha agregado la IP {ip}')
    send_message(f'Se ha agregado la IP {ip}')

def show_ips(update, context):
    ip_list = get_ip_list()

    if ip_list:
        ips = ""
        for ip in ip_list:
            ips += f"[ INFO ] IP: {ip}\n"
        update.message.reply_text(f'Las siguientes IPs están registradas:\n{ips}')
    else:
        update.message.reply_text(f'[ INFO ] Aun no se han cargado ips.')

def remove_ip(update, context):
    ip_to_remove = context.args[0]
    ip_list = get_ip_list()

    with open("ip_list.txt", 'w') as ip_list_file:
        exists = False
        for ip in ip_list:
            if ip == ip_to_remove:
                exists = True
                update.message.reply_text(f'[ INFO ] Se quito la ip: {ip_to_remove}.')
            else:
                ip_list_file.write(ip + "\n")
        if not exists:
            update.message.reply_text(f'⚠⚠⚠ [ WARNING ] No se encontro la ip: {ip_to_remove}.')

def help(update, context):
    command_list = """
    Lista de comandos:\n
    /addip xxx.xxx.xxx.xxx (Agrega una ip)
    /showips (Muestra las ips agregadas)
    /removeip xxx.xxx.xxx.xxx (Elimina una ip de la lista)
    /help (Muestra este mensaje)
    """
    update.message.reply_text(command_list)

def send_message(message):
    bot = Updater(TOKEN).bot
    bot.send_message(chat_id=ROOM_ID, text=message)

updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher
addip_handler = CommandHandler('addip', add_ip)
dispatcher.add_handler(addip_handler)
showips_handler = CommandHandler('showips', show_ips)
dispatcher.add_handler(showips_handler)
removeip_handler = CommandHandler('removeip', remove_ip)
dispatcher.add_handler(removeip_handler)
help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)
schedule.every(CHECK_IPS_INTERVAL).seconds.do(report_ip_address_status)

WELCOME_MESSAGE = f"""
Hola, soy Pinger@Bot! 🤗
Me han configurado para reportar direcciones
ip que no responden.
Cada {CHECK_IPS_INTERVAL} segundos, voy a estar mirando si alguna ip no responde. 
Veamos que tenemos... 👀
Ejecuta /help para ver las opciones... 😁
"""
send_message(WELCOME_MESSAGE)


while True:
    schedule.run_pending()
    updater.start_polling()
    time.sleep(1)
