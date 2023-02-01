import telebot as tl
from telebot import types
from databaseF import Database

db=Database('db.db3')
bot=tl.TeleBot('5669265039:AAEfAtDMJ_YpphPLJmoSrY0UhWDVBSmsFKM')
name = ''
anketa=''
age = 0
gend=''
description=''
flag=False
inDialog=False
flagFirst=0
idphoto=None
@bot.message_handler(commands=['start','reg'])
def start(message):
    global anket
    global flag
    anketa=''
    if message.text == '/reg':
        flag=False
        bot.send_message(message.from_user.id, "Как тебя зовут?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg')

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Отправьте фото на аватарку')
    bot.register_next_step_handler(message, get_gender1)

def get_gender1(message):
    global idphoto
    idphoto = message.photo[0].file_id
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
        bot.send_message(message.from_user.id, 'Напиши пару слов о себе. Креатив - залог успеха)',reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, get_desc)
    else:
        bot.send_message(message.chat.id, 'Нажми на кнопку ниже - парень или девушка')
        bot.register_next_step_handler(message, get_gender1)

def get_desc(message):
    global description
    description=message.text
    bot.send_message(message.chat.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_age)

    
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
    global description
    if message.chat.type=='private':
        if message.text=='Да':
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton('Поиск собеседника')
            markup.add(item1)
            flag=True
            if name!='' and age!=0 and gend!='' and flag:
                db.add_user(message.chat.id, gend, age, name,description)
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
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('Поиск собеседника')
        markup.add(item1)
        bot.send_message(message.chat.id, 'Вы не начали чат!',reply_markup=markup)    

@bot.message_handler(content_types=['text'])
def main(message):
    global flag
    global anketa
    global flagFirst
    global inDialog
    if message.chat.type=='private' and flag:
        if message.text=='Поиск собеседника':
            markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1=types.KeyboardButton('Остановить поиск')
            markup.add(item1)
            chat_two=db.get_chat()#берем второго собеседника. Стоит первым в очереди
            if db.create_chat(message.chat.id, chat_two)==False:
                db.add_queue(message.chat.id)
                inDialog=False
                flagFirst=0
                bot.send_message(message.chat.id,'Идет поиск собеседника',reply_markup=markup)
            else:
                mess='Собеседник найден! Чтобы остановить диалог, нажмите /stop' 
                markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
                #item1=types.KeyboardButton('Отправить ссылку на мою страницу')
                inDialog=True
                item1=types.KeyboardButton('/stop')
                markup.add(item1)
                bot.send_message(message.chat.id,mess,reply_markup=markup)
                bot.send_message(chat_two,mess,reply_markup=markup)
                chat_info=db.get_active_chat(message.chat.id)
                #db.de()
                myname,myage,mygender,mydesc= db.create_self_anketa(message.chat.id)
                anketa=myname + ', ' + str(myage) + ', '+ mygender + '\n' +mydesc 
                bot.send_message(chat_info[1],anketa)
                flagFirst+=1
                bot.send_message(message.chat.id,'Вы отправили анкету собеседнику')                
        elif message.text =='Остановить поиск' and inDialog==False:
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id,'Поиск остановлен, напишите Поиск собеседника',reply_markup=types.ReplyKeyboardRemove())
        elif inDialog:
            chat_info=db.get_active_chat(message.chat.id)
            bot.send_message(chat_info[1],message.text)
            if flagFirst<2:
                flagFirst+=1
                myname,myage,mygender,mydesc= db.create_self_anketa(message.chat.id)
                anketa=myname + ', ' + str(myage) + ', '+ mygender + '\n' +mydesc 
                bot.send_message(chat_info[1],anketa)
        else:
            bot.send_message(message.chat.id,'Вы не в диалоге. Найдите собеседника')
    else:
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton('/reg')
        markup.add(item1)
        bot.send_message(message.chat.id,' Вы не зарегестрированы, напишите /reg',reply_markup=markup)

#@bot.message_handler(content_types=["photo"])
#def photo(message):
 #  idphoto = message.photo[0].file_id
   #bot.send_photo(message.chat.id, idphoto )

bot.polling(none_stop=True,interval=0)
