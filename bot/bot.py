import telebot as tl
from telebot import types
from database import Database

db=Database('db.db3')
bot=tl.TeleBot('5669265039:AAEfAtDMJ_YpphPLJmoSrY0UhWDVBSmsFKM')
name = ''
surname = ''
age = 0
@bot.message_handler(commands=['start','reg'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)
    
def get_age(message):
    global age
    try:
        age = int(message.text)
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_age)
        return None
    #keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    #key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes') #кнопка «Да»
    #keyboard.add(key_yes) #добавляем кнопку в клавиатуру
    #key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
    #keyboard.add(key_no)
    question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' ?'
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton('Да')
    item2=types.KeyboardButton('Нет')
    markup.add(item1,item2)
    bot.send_message(message.from_user.id, text=question.format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, menu)
    
@bot.message_handler(commands=['menu'])
#@bot.message_handler(content_types=['text'])
def menu(message):
    if message.chat.type=='private':
        print(message.text)
        if message.text=='Да':
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton('Поиск собеседника')
            markup.add(item1)
            bot.send_message(message.from_user.id, 'Выберете команду'.format(message.from_user),reply_markup=markup)
            bot.register_next_step_handler(message, end_regestration)
        elif message.text=='Нет':
            bot.send_message(message.chat.id, 'Напишите /reg')

def end_regestration(message):
    if message.chat.type=='private':
            if message.text=='Поиск собеседника':
                markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                print('Добавили в базу')
                item1=types.KeyboardButton('Остановить поиск')
                markup.add(item1)
                db.add_queue(message.chat.id)
                bot.send_message(message.chat.id,'Идет поиск собеседника',reply_markup=markup)
            elif message.text =='Остановить поиск':
                print('Удалили из базы')
                db.delete_queue(message.chat.id)
                bot.send_message(message.chat.id,'Поиск остановлен, напишите /menu')
            else:
                print('Вы на этапе Где уже заносится в базу и тд')






















        
'''
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
         #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Спасибо за регистрацию')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Пройди регистрацию заново. Напиши /reg')
'''


bot.polling(none_stop=True,interval=0)
