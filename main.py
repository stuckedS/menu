import os
from background import keep_alive  #импорт функции для поддержки работоспособности
import pip

pip.main(['install', 'pytelegrambotapi'])
pip.main(['install', 'openpyxl'])
import telebot
import time
from telebot import types
import pandas as pd
bot = telebot.TeleBot('6050263932:AAEi5P7YT-JTf6VT7jOWfu_YOn8q5ANQWO0')

df = pd.concat(pd.read_excel(r'Новое учебное меню.xlsx', sheet_name=None),
               ignore_index=True)

df.drop(columns=df.columns[0], axis=1, inplace=True)
df.drop(columns=df.columns[1], axis=1, inplace=True)
df = df.to_dict('dict')

da = pd.concat(pd.read_excel(r'Глоссарий.xlsx', sheet_name=None),
               ignore_index=True)
da = da.to_dict('dict')

@bot.message_handler(commands=['start'])
def menu(message):
  start_menu = types.ReplyKeyboardMarkup(True, True)
  start_menu.row('Глоссарий')
  bot.send_message(message.chat.id,
                   'Для поиска введите начало названия блюда',
                   reply_markup=start_menu)


@bot.message_handler(content_types=['text'])
def handle_text(message):
  if message.text == 'Глоссарий':
    messg = bot.send_message(message.chat.id, 'Глоссарий')  
    bot.register_next_step_handler(messg,gloss)
  else:
    matches = [
      x for x in df['Unnamed: 1'].values()
      if isinstance(x, str) and message.text in x
    ]
    match = ' '.join(matches)
    if len(matches) > 1:
      bot.send_message(message.chat.id, match)
      podtip = types.ReplyKeyboardMarkup(True, True)
      for i in matches:
        podtip.row(i)
      bot.send_message(message.chat.id, 'Выберите', reply_markup=podtip)  
      
    matches = ''.join(matches)

    def get_key(d, value):
      for k, v in d.items():
        if v == value:
          return k


  
    key = get_key(df['Unnamed: 1'], matches)
    print(df['Unnamed: 1'].get(key))
    bot.send_message(message.chat.id, df['Unnamed: 3'].get(key))
    bot.send_message(message.chat.id, df['Unnamed: 4'].get(key))
    menu(message) 
def gloss(message):
  matches = [
      x for x in da['Unnamed: 1'].values()
      if isinstance(x, str) and message.text in x
    ]
  match = ' '.join(matches)
  if len(matches) > 1:
    bot.send_message(message.chat.id, match)
    podtip = types.ReplyKeyboardMarkup(True, True)
    for i in matches:
      podtip.row(i)
    msg=bot.send_message(message.chat.id, 'Выберите', reply_markup=podtip)  
    bot.register_next_step_handler(msg,gloss) 
  matches = ''.join(matches)

  def get_key(d, value):
    for k, v in d.items():
      if v == value:
        return k


  
  key = get_key(da['Unnamed: 1'], matches)
  bot.send_message(message.chat.id, da['Unnamed: 2'].get(key))
  menu(message) 
  


keep_alive()  #запускаем flask-сервер в отдельном потоке. Подробнее ниже...
bot.polling(non_stop=True, interval=0)  #запуск бота
