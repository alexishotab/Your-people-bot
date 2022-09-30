import telebot as tl
from telebot import types
from databaseF import Database

db=Database('db.db3')
bot=tl.TeleBot('5669265039:AAEfAtDMJ_YpphPLJmoSrY0UhWDVBSmsFKM')
name = ''
age = 0
gend=''
flag=False
@bot.message_handler(commands=['start','reg'])
def start(message):
    global flag
    if message.text == '/reg':
        flag=False
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message):
    global name
    name = message.text
    bot.register_next_step_handler(message, get_gender1)

def get_gender1(message):    
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton('Парень')
    item2=types.KeyboardButton('Девушка')
    markup.add(item1,item2)
    bot.send_message(message.from_user.id, 'Выбери свой пол. Нажми на кнопку ниже',reply_markup=markup)
    bot.register_next_step_handler(message, get_gender)

def get_gender(message):
    global gend
    if message.text=='Парень' or message.text=='Девушка':
        gend=message.text
        bot.send_message(message.from_user.id, 'Сколько тебе лет?')
        bot.register_next_step_handler(message, get_age)
    else:
        bot.send_message(message.chat.id, 'Нажми на кнопку ниже - парень или девушка')
        bot.register_next_step_handler(message, get_gender1)
    
def get_age(message):
    global age
    try:
        age = int(message.text)
    except Exception:
        bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
        bot.register_next_step_handler(message, get_age)
        return None
    question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' ?'
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton('Да')
    item2=types.KeyboardButton('Нет')
    markup.add(item1,item2)
    bot.send_message(message.from_user.id, text=question.format(message.from_user), reply_markup=markup)
    bot.register_next_step_handler(message, menu)
    
def menu(message):
    global flag
    global name
    global gend
    if message.chat.type=='private':
        if message.text=='Да':
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton('Поиск собеседника')
            markup.add(item1)
            flag=True
            if name!='' and age!=0 and gend!='' and flag:
                db.add_user(message.chat.id, gend, age, name)
                bot.send_message(message.from_user.id, 'Вы создали анкету, поздравляем!'.format(message.from_user),reply_markup=markup)            
            else:
                print(name,age,gend,flag,chat_id)
        elif message.text=='Нет':
            bot.send_message(message.chat.id, 'Напишите /reg')
            flag=False

@bot.message_handler(commands=['stop'])
def stop(message):
    chat_info=db.get_active_chat(message.chat.id)
    if chat_info!=False:
        db.delete_chat(chat_info[0])
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('Поиск собеседника')
        markup.add(item1)
        bot.send_message(chat_info[1], 'Собеседник покинул чат',reply_markup=markup)
        bot.send_message(message.chat.id, 'Вы вышли из чата',reply_markup=markup)    
    else:
        bot.send_message(message.chat.id, 'Вы не начали чат!',reply_markup=markup)    

@bot.message_handler(content_types=['text'])
def main(message):
    global flag
    if message.chat.type=='private' and flag:
        if message.text=='Поиск собеседника':
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton('5Остановить поиск')
            markup.add(item1)
            chat_two=db.get_chat()#берем второго собеседника. Стоит первым в очереди
            if db.create_chat(message.chat.id, chat_two)==False:
                db.add_queue(message.chat.id)
                bot.send_message(message.chat.id,'Идет поиск собеседника',reply_markup=markup)
            else:
                mess='Собеседник найден! Чтобы остановить диалог, нажмите /stop' 
                markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1=types.KeyboardButton('/stop')
                markup.add(item1)
                bot.send_message(message.chat.id,mess,reply_markup=markup)
                bot.send_message(chat_two,mess,reply_markup=markup)
        elif message.text =='Остановить поиск':
            print('Удалили из базы')
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id,'Поиск остановлен, напишите /menu')
        else:
            chat_info=db.get_active_chat(message.chat.id)
            myname,myage,mygender= db.create_self_anketa(message.chat.id)
            anketa=myname + ', ' + str(myage) + ', '+ mygender + ' привет'
            bot.send_message(chat_info[1],anketa)
            #opname,opage,opgender=db.create_self_anketa(chat_info[1])
            #bot.send_message(chat_info[1],message.text)
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('/reg')
        markup.add(item1)
        bot.send_message(message.chat.id,' Вы не зарегестрированы, напишите /reg',reply_markup=markup)






















        
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
