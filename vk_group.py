import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import datetime
import json
import sqlite3
import asyncio

vk_session = vk_api.VkApi(
    token='9ee8528a5486ff195b298ba1a30994c98def107c137d8a2a058c26df9127c21487f7843bb399e51d9fd08')

longpoll = VkBotLongPoll(vk_session, '193164016')
comand_lst = ['!статус', '!Россия']
key_words = ['PUBG', 'Fortnite', 'Dota 2', 'CSGO', 'Ранг', 'Кол-во часов', 'Ссылка на стр вк', 'Меню режимов']
setting_words = ['Смотреть анкеты', 'Создать свою']
csgo_rangs = ['Сильвер', 'Звёзды', 'Калаши', 'Бигастар - Лем', 'Суприм - Глобал']
csgo_hours = ["100-500", "500-800", "800-1000", "1000 - 1500", "1500+"]
rang_csgo_flag = False
csgo_flag = True
lst_flag = False
menu_flag = True
vk = vk_session.get_api()
con = sqlite3.connect('db/csgo.sqlite3')
cur = con.cursor()


async def send_msg(event):
    global menu_flag
    vk.messages.send(user_id=event.obj.from_id,
                     random_id=random.randint(0, 2 ** 64),
                     message=f"Выберите режим",
                     keyboard=json.dumps(menu_keyboard, ensure_ascii=False)
                     )
    menu_flag = False


async def send_profile(event):

    profiles = cur.execute('''SELECT * from csgo  WHERE vk_id is not Null''').fetchall()
    user_id = event.obj.message['from_id']
    stroka = f"Ранг - {profiles[cur.execute('''SELECT counter from csgo WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][1]}, Колличество часов - {profiles[cur.execute('''SELECT counter from csgo WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][2]}"
    vk.messages.send(user_id=user_id,
                     random_id=random.randint(0, 2 ** 64),
                     message=stroka,
                     keyboard=json.dumps(like_keyboard, ensure_ascii=False))


async def game_choose(event):

    vk.messages.send(user_id=event.obj.message['from_id'],
                     random_id=random.randint(0, 2 ** 64),
                     message=f"Выберите игру:",
                     keyboard=json.dumps(keyboard, ensure_ascii=False))

async def send_id(event):
    profiles = cur.execute('''SELECT * from csgo  WHERE vk_id is not Null''').fetchall()
    profile = profiles[cur.execute('''SELECT counter from csgo WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][0]
    vk.messages.send(user_id=event.obj.message['from_id'],
                     random_id=random.randint(0, 2 ** 64),
                     message=f'Профиль игрока: {profile}',
                     keyboard=json.dumps(like_keyboard, ensure_ascii=False))
async def watch_profiless(event):
    first_flag = True
    await send_profile(event)
    send_flag = True

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            cur.execute('''UPDATE csgo
                                                SET last_msg = ?
                                                WHERE vk_id = ?''', (
                event.obj.message['text'],
                'https://vk.com/id' + str(event.obj.message['from_id']),))
            counter = cur.execute('''SELECT counter from csgo WHERE vk_id = ?''',
                                  ('https://vk.com/id' + str(
                                      event.obj.message['from_id']),)).fetchall()
            txt = event.obj.message['text']
            try:
                if cur.execute('''SELECT last_msg FROM csgo WHERE vk_id = ?''',
                               ('https://vk.com/id' + str(
                                   event.obj.message['from_id']),)).fetchall()[0][
                    0] == 'Понравилось' and \
                        cur.execute('''SELECT last_msg FROM csgo WHERE vk_id = ?''',
                                    ('https://vk.com/id' + str(
                                        event.obj.message['from_id']),)).fetchall()[0][
                            0] != 'Меню режимов':
                    print(cur.execute('''SELECT last_msg FROM csgo WHERE vk_id = ?''',
                                      ('https://vk.com/id' + str(
                                          event.obj.message['from_id']),)).fetchall()[0][
                              0])
                    await send_id(event)
                    cur.execute('''UPDATE csgo 
                                                        SET counter = counter + 1
                                                        WHERE vk_id = ?''',
                                ('https://vk.com/id' + str(
                                    event.obj.message['from_id']),)).fetchall()
                    counter = \
                        cur.execute('''SELECT counter from csgo WHERE vk_id = ?''',
                                    ('https://vk.com/id' + str(
                                        event.obj.message['from_id']),)).fetchall()[
                            0][0]
                elif cur.execute('''SELECT last_msg FROM csgo WHERE vk_id = ?''',
                                 ('https://vk.com/id' + str(
                                     event.obj.message['from_id']),)).fetchall()[
                    0][0] == 'Не понравилось' and \
                        cur.execute('''SELECT last_msg FROM csgo WHERE vk_id = ?''',
                                    ('https://vk.com/id' + str(
                                        event.obj.message['from_id']),)).fetchall()[0][
                            0] != 'Меню режимов':
                    cur.execute('''UPDATE csgo 
                                                           SET counter = counter + 1
                                                           WHERE vk_id = ?''',
                                ('https://vk.com/id' + str(
                                    event.obj.message['from_id']),)).fetchall()
                    counter = cur.execute('''SELECT counter from csgo WHERE vk_id = ?''', (
                        'https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]
                elif cur.execute('''SELECT last_msg FROM csgo WHERE vk_id = ?''',
                                 ('https://vk.com/id' + str(
                                     event.obj.message['from_id']),)).fetchall()[0][
                    0] == 'Меню режимов':
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     message=f"Выберите режим",
                                     keyboard=json.dumps(menu_keyboard, ensure_ascii=False)
                                     )
                    cur.execute('''UPDATE csgo 
                                                            SET counter = 0
                                                            WHERE vk_id = ?''',
                                ('https://vk.com/id' + str(
                                    event.obj.message['from_id']),)).fetchall()
                    send_flag = False
                    con.commit()
            except IndexError:
                pass
            try:
                if send_flag:
                    await send_profile(event)
            except IndexError:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 random_id=random.randint(0, 2 ** 64),
                                 message=f"Анкет больше нету")
                cur.execute('''UPDATE csgo 
                                                        SET counter = 0
                                                        WHERE vk_id = ?''',
                            ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()

            con.commit()
like_keyboard = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Понравилось"
            },
            "color": "positive"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Не понравилось"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Меню режимов"
                },
                "color": "positive"
            }
        ]
    ]
}
menu_keyboard = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Смотреть анкеты"
            },
            "color": "positive"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Создать свою"
                },
                "color": "primary"
            },
        ]
    ]
}
keyboard = {
    "one_time": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "CSGO"
            },
            "color": "negative"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Dota 2"
                },
                "color": "positive"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Fortnite"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "PUBG"
                },
                "color": "secondary"
            }
        ]
    ]
}

csgo_keyboard = {
    "one_time": False,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"2\"}",
                "label": "Ранг"
            },
            "color": "positive"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Кол-во часов"
                },
                "color": "primary"
            },
        ]
    ]
}

csgo_hours_keyboard = {
    "one_time": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "100-500"
            },
            "color": "negative"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "500-800"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "800-1000"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "1000-1500"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "1500+"
                },
                "color": "primary"
            },
        ]
    ]
}
csgo_rang_keyboard = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Сильвер"
                },
                "color": "negative"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Звёзды"
                },
                "color": "positive"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Калаши"
                },
                "color": "primary"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "Бигастар - Лем"
                },
                "color": "secondary"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Суприм - Глобал"
                }
            }
        ]
    ]
}


async def main():
    rang_csgo_flag = False
    csgo_flag = True
    lst_flag = False
    menu_flag = True
    profiles_flag = True
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            if menu_flag:
                await send_msg(event)
        if event.type == VkBotEventType.MESSAGE_NEW:
            cur.execute('''UPDATE csgo
                        SET last_msg = ?
                        WHERE vk_id = ?''',
                        (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))
            con.commit()
            rank = ''
            txt = event.obj.message['text']
            if txt not in comand_lst and txt not in key_words:
                try:
                    if cur.execute('''SELECT last_msg FROM csgo WHERE vk_id = ?''',
                                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
                        0] == 'Смотреть анкеты' and profiles_flag:
                        await watch_profiless()
                except IndexError:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     message="Сначала зарегестрируйтесь",
                                     random_id=random.randint(0, 2 ** 64))

                    await game_choose(event)
            if event.obj.message['text'] == 'Создать свою':
                print(txt)
                await game_choose(event)
                lst_flag = True

            if event.obj.message['text'] == '!статус':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Пока что пользуетесь ботом через лс",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'] == 'CSGO' and lst_flag:
                try:
                    result = cur.execute('''INSERT INTO csgo(vk_id, counter) 
                                            VALUES(?, ?)''',
                                         ('https://vk.com/id' + str(event.obj.message['from_id']), 0,))
                    con.commit()
                    csgo_flag = True
                except sqlite3.IntegrityError:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     message='Такой пользоватьель уже есть',
                                     keyboard=json.dumps(keyboard, ensure_ascii=False))
                    csgo_flag = False
                if csgo_flag:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     message=f"Дайте информацию",
                                     keyboard=json.dumps(csgo_keyboard, ensure_ascii=False))
                if csgo_flag:
                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW:
                            txt = event.obj.message['text']
                            if event.obj.message['text'] == 'Ранг' and csgo_flag:
                                if len('https://vk.com/id' + str(event.obj.message['from_id'])) == 0:
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     random_id=random.randint(0, 2 ** 64),
                                                     message=f"Сначала дайте свою ссылку на страницу в вк")
                                else:
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     random_id=random.randint(0, 2 ** 64),
                                                     message=f"Выберите ранг",
                                                     keyboard=json.dumps(csgo_rang_keyboard, ensure_ascii=False))
                            if event.obj.message['text'] in csgo_rangs and csgo_flag:
                                rank = txt
                                result = cur.execute('''UPDATE csgo
                                                        SET rank = ?
                                                        WHERE vk_id = ?''',
                                                     (txt, 'https://vk.com/id' + str(event.obj.message['from_id']),))
                                con.commit()
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 random_id=random.randint(0, 2 ** 64),
                                                 message=f"Дайте информацию",
                                                 keyboard=json.dumps(csgo_keyboard, ensure_ascii=False))
                            if event.obj.message['text'] == 'Кол-во часов' and csgo_flag:
                                if len(rank) > 0:
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     random_id=random.randint(0, 2 ** 64),
                                                     message='Выберите кол-во часов',
                                                     keyboard=json.dumps(csgo_hours_keyboard, ensure_ascii=False))
                                else:
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     random_id=random.randint(0, 2 ** 64),
                                                     message='Сначала скажите свой ранг')
                                rang_csgo_flag = True
                            if event.obj.message['text'] in csgo_hours:
                                result = cur.execute('''UPDATE csgo
                                                        SET hours = ?
                                                        WHERE vk_id = ?''',
                                                     (txt, 'https://vk.com/id' + str(event.obj.message['from_id']),))
                                con.commit()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
