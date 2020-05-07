import random,telebot,os,webbrowser,pyautogui,time
from PIL import Image, ImageGrab



mytoken = 'telegram token'

bot = telebot.TeleBot(mytoken)


mainkeyboard = telebot.types.ReplyKeyboardMarkup(True, True)

mainkeyboard.row('/off','/open','/screen')




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
