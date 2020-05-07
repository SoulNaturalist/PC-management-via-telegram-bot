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


        if message.text == '/open':
                bot.register_next_step_handler(message,get_url)
                bot.send_message(message.chat.id,'Отправьте ссылку!')
                

        if message.text == '/screen':
                try:  
                        os.remove("screenshot.png")
                except:
                        bot.send_message(message.chat.id,'Делаю скриншот')
                        screen = pyautogui.screenshot('screenshot.png')
                        screen = open('screenshot.png', 'rb')
                        bot.send_photo(message.chat.id, screen)
                




def get_url(message):
        global url
        url = message.text
        webbrowser.open_new(url)
        bot.send_message(message.chat.id,'Ссылка открыта!')


try:
        bot.polling(none_stop=True, interval=0)
except:
        pass
