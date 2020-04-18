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
create_profile_words = ['RL', 'Fortnite', 'Dota 2', 'CSGO', 'Ранг', 'Кол-во часов', 'Ссылка на стр вк', "100-500",
                        "500-800", "800-1000", "1000 - 1500", "1500+", 'Сильвер', 'Звёзды', 'Калаши', 'Бигастар - Лем',
                        'Суприм - Глобал', 'Prospect 1 - Prospect elite', 'challenger 1 - challenger elite',
                        'rising star - champion']
games = ['RL', 'Fortnite', 'Dota 2', 'CSGO']
like_words = ['Понравилось', 'Не понравилось']
setting_words = ['смотреть CSGO', 'смотреть RL']
csgo_rangs = ['Сильвер', 'Звёзды', 'Калаши', 'Бигастар - Лем', 'Суприм - Глобал']
hours = ["100-500", "500-800", "800-1000", "1500+"]
rl_rangs = ['Prospect 1 - Prospect elite', 'challenger 1 - challenger elite', 'rising star - champion']
rang_csgo_flag = False
csgo_flag = True
lst_flag = False
menu_flag = True
vk = vk_session.get_api()
con = sqlite3.connect('db/csgo.sqlite3')
cur = con.cursor()

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
                    "label": "RL"
                },
                "color": "secondary"
            }
        ]
    ]
}

csgo_keyboard = {
    "one_time": True,
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

hours_keyboard = {
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
watch_keyboard = {
    "one_time": True,
    "buttons": [
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"1\"}",
                "label": "смотреть CSGO"
            },
            "color": "negative"
        },

            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "смотреть RL"
                },
                "color": "secondary"
            }
        ]
    ]
}
rl_rang_keyboard = {
    "one_time": True,
    "buttons": [
        [
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"1\"}",
                    "label": "Prospect 1 - Prospect elite"
                },
                "color": "negative"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "challenger 1 - challenger elite"
                },
                "color": "positive"
            },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"2\"}",
                    "label": "rising star - champion"
                },
                "color": "primary"
            }
        ]
    ]
}


def chek_profile(vk_id, game=None):
    if game == 'CSGO':
        flag = True
        try:
            profiles = cur.execute('''SELECT * from csgo WHERE vk_id = ?''', (vk_id,)).fetchall()[0]
            for i in range(len(profiles)):
                if profiles[i] is None:
                    flag = flag and False
        except IndexError:
            flag = False
        return flag
    elif game == 'rl':

        flag = True
        try:
            profiles = cur.execute('''SELECT * from rl WHERE vk_id = ?''', (vk_id,)).fetchall()[0]
            print(profiles)
            for i in range(len(profiles)):
                if profiles[i] is None:
                    flag = flag and False
        except IndexError:
            flag = False
        return flag


async def send_msg(event):
    global menu_flag
    vk.messages.send(user_id=event.obj.from_id,
                     random_id=random.randint(0, 2 ** 64),
                     message=f"Выберите режим",
                     keyboard=json.dumps(menu_keyboard, ensure_ascii=False)
                     )
    menu_flag = False


async def send_profile(event, game):
    if game == 'csgo':
        profiles = cur.execute('''SELECT * from csgo  WHERE vk_id is not Null''').fetchall()
        user_id = event.obj.message['from_id']
        stroka = f"Ранг - {profiles[cur.execute('''SELECT counter from csgo WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][1]}, Колличество часов - {profiles[cur.execute('''SELECT counter from rl WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][2]}"
    elif game == 'rl':
        profiles = cur.execute('''SELECT * from rl  WHERE vk_id is not Null''').fetchall()
        user_id = event.obj.message['from_id']
        stroka = f"Ранг - {profiles[cur.execute('''SELECT counter from rl WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][1]}, Колличество часов - {profiles[cur.execute('''SELECT counter from rl WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][2]}"
    vk.messages.send(user_id=user_id,
                     random_id=random.randint(0, 2 ** 64),
                     message=stroka,
                     keyboard=json.dumps(like_keyboard, ensure_ascii=False))
    cur.execute('''UPDATE msg SET msg_flag = 1 WHERE vk_id = ?''',
                ('https://vk.com/id' + str(event.obj.message['from_id']),))

async def game_choose(event):
    if event.obj.message is None:
        vk.messages.send(user_id=event.obj['peer_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите игру:",
                         keyboard=json.dumps(keyboard, ensure_ascii=False))
    else:
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите игру:",
                         keyboard=json.dumps(keyboard, ensure_ascii=False))


async def send_id(event, game):
    if game == 'csgo':
        profiles = cur.execute('''SELECT * from csgo  WHERE vk_id is not Null''').fetchall()
        profile = profiles[cur.execute('''SELECT counter from csgo WHERE vk_id = ?''',
                                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][0]
    elif game == 'rl':
        profiles = cur.execute('''SELECT * from rl  WHERE vk_id is not Null''').fetchall()
        profile = profiles[cur.execute('''SELECT counter from rl WHERE vk_id = ?''',
                                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][0]
    vk.messages.send(user_id=event.obj.message['from_id'],
                     random_id=random.randint(0, 2 ** 64),
                     message=f'Профиль игрока: {profile}',
                     keyboard=json.dumps(like_keyboard, ensure_ascii=False))
    cur.execute('''UPDATE msg SET msg_flag = 1 WHERE vk_id = ?''',
                ('https://vk.com/id' + str(event.obj.message['from_id']),))


def csgo_profile(event):
    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == 'Ранг' and cur.execute('''SELECT csgo_flag FROM csgo WHERE vk_id = ?''',
                                     ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == '1':
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите ранг",
                         keyboard=json.dumps(csgo_rang_keyboard, ensure_ascii=False))
    if event.obj.message['text'] in csgo_rangs and cur.execute('''SELECT csgo_flag FROM csgo WHERE vk_id = ?''', (
            'https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == '1':
        rank = event.obj.message['text']
        result = cur.execute('''UPDATE csgo
                                        SET rank = ?
                                        WHERE vk_id = ?''',
                             (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message='Колличество часов',
                         keyboard=json.dumps(csgo_keyboard, ensure_ascii=False))
        con.commit()
    if event.obj.message['text'] == 'Кол-во часов' and cur.execute('''SELECT csgo_flag FROM csgo WHERE vk_id = ?''',
                                                                   ('https://vk.com/id' + str(event.obj.message[
                                                                                                  'from_id']),)).fetchall()[
        0][0] == '1':
        if cur.execute('''SELECT rank FROM csgo WHERE vk_id = ?''',
                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] is not None:

            vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message='Выберите кол-во часов',
                             keyboard=json.dumps(hours_keyboard, ensure_ascii=False))
        else:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message='Сначала скажите свой ранг')
    if event.obj.message['text'] in hours:
        result = cur.execute('''UPDATE csgo
                                        SET hours = ?
                                        WHERE vk_id = ?''',
                             (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите режим",
                         keyboard=json.dumps(menu_keyboard, ensure_ascii=False)
                         )
        cur.execute('''UPDATE msg
                        SET create_game = ?
                        WHERE vk_id = ?''',
                             (None, 'https://vk.com/id' + str(event.obj.message['from_id']),))
        con.commit()


def csgo(event):
    cur.execute('''UPDATE msg
                SET last_msg = ?
                WHERE vk_id = ?''', (
        event.obj.message['text'],
        'https://vk.com/id' + str(event.obj.message['from_id']),))
    try:
        cur.execute('''INSERT INTO csgo(vk_id, csgo_flag, lst_flag, counter) VALUES(?, 1, 1, 0)''',
                    ('https://vk.com/id' + str(event.obj.message['from_id']),))
        con.commit()
    except sqlite3.IntegrityError:
        if chek_profile('https://vk.com/id' + str(event.obj.message['from_id'])):
            vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message='Такой пользоватьель уже есть',
                             keyboard=json.dumps(menu_keyboard, ensure_ascii=False))
            cur.execute('''UPDATE csgo
                            SET csgo_flag = 0
                            WHERE vk_id = ?''',
                        ('https://vk.com/id' + str(event.obj.message['from_id']),))

    if cur.execute('''SELECT csgo_flag FROM csgo WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == '1' and \
            cur.execute('''SELECT lst_flag FROM csgo WHERE vk_id = ?''',
                        ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == '1':
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Дайте информацию",
                         keyboard=json.dumps(csgo_keyboard, ensure_ascii=False))
        cur.execute('''UPDATE csgo
                        SET lst_flag = 0
                        WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),))

    if cur.execute('''SELECT csgo_flag FROM csgo WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == '1':
        txt = event.obj.message['text']
        csgo_profile(event)


def rl(event):
    cur.execute('''UPDATE msg
                SET last_msg = ?
                WHERE vk_id = ?''', (
        event.obj.message['text'],
        'https://vk.com/id' + str(event.obj.message['from_id']),))
    try:
        cur.execute('''INSERT INTO rl(vk_id, rl_flag, lst_flag, counter) VALUES(?, 1, 1, 0)''',
                    ('https://vk.com/id' + str(event.obj.message['from_id']),))
        con.commit()
    except sqlite3.IntegrityError:
        if chek_profile('https://vk.com/id' + str(event.obj.message['from_id'])):
            vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message='Такой пользоватьель уже есть',
                             keyboard=json.dumps(menu_keyboard, ensure_ascii=False))
            cur.execute('''UPDATE rl
                            SET rl_flag = 0
                            WHERE vk_id = ?''',
                        ('https://vk.com/id' + str(event.obj.message['from_id']),))
            con.commit()

    if cur.execute('''SELECT lst_flag FROM rl WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == '1' and \
            cur.execute('''SELECT rl_flag FROM rl WHERE vk_id = ?''',
                        ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == 1:
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Дайте информацию",
                         keyboard=json.dumps(csgo_keyboard, ensure_ascii=False))
        cur.execute('''UPDATE rl
                        SET lst_flag = 0
                        WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),))
    if cur.execute('''SELECT rl_flag FROM rl WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == 1:
        txt = event.obj.message['text']
        rl_profile(event)


def rl_profile(event):
    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == 'Ранг' and cur.execute('''SELECT rl_flag FROM rl WHERE vk_id = ?''',
                                     ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == 1:
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите ранг",
                         keyboard=json.dumps(rl_rang_keyboard, ensure_ascii=False))
    if event.obj.message['text'] in rl_rangs and cur.execute('''SELECT rl_flag FROM rl WHERE vk_id = ?''', (
            'https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == 1:
        rank = event.obj.message['text']
        result = cur.execute('''UPDATE rl
                                        SET rank = ?
                                        WHERE vk_id = ?''',
                             (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message='Колличество часов',
                         keyboard=json.dumps(csgo_keyboard, ensure_ascii=False))
        con.commit()
    if event.obj.message['text'] == 'Кол-во часов' and cur.execute('''SELECT rl_flag FROM rl WHERE vk_id = ?''',
                                                                   ('https://vk.com/id' + str(event.obj.message[
                                                                                                  'from_id']),)).fetchall()[
        0][0] == 1:
        if cur.execute('''SELECT rank FROM rl WHERE vk_id = ?''',
                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] is not None:

            vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message='Выберите кол-во часов',
                             keyboard=json.dumps(hours_keyboard, ensure_ascii=False))
        else:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message='Сначала скажите свой ранг')
    if event.obj.message['text'] in hours:
        result = cur.execute('''UPDATE rl
                                        SET hours = ?
                                        WHERE vk_id = ?''',
                             (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите режим",
                         keyboard=json.dumps(menu_keyboard, ensure_ascii=False)
                         )
        con.commit()


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
            try:
                cur.execute('''INSERT INTO msg(vk_id, last_msg) 
                                                VALUES(?, ?)''',
                            ('https://vk.com/id' + str(event.obj.message['from_id']), event.obj.message['text'],))

            except sqlite3.IntegrityError:
                cur.execute('''UPDATE msg
                            SET last_msg = ?
                            WHERE vk_id = ?''',
                            (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))
            con.commit()
            rank = ''
            txt = event.obj.message['text']
            if txt not in comand_lst and txt not in like_words and txt not in create_profile_words or txt in setting_words:
                try:
                    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == \
                            'Смотреть анкеты' or txt in setting_words:

                        cur.execute('''UPDATE msg
                                        SET watch_flag = 1
                                        WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),))
                        print(type(cur.execute('''SELECT msg_flag FROM msg WHERE vk_id = ?''',
                                               ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[
                                       0][
                                       0]))
                        if cur.execute('''SELECT msg_flag FROM msg WHERE vk_id = ?''',
                                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
                            0] == None:
                            chek_profile('https://vk.com/id' + str(event.obj.message['from_id']), "CSGO")
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             random_id=random.randint(0, 2 ** 64),
                                             message=f"Сначала зарегестрируйстесь")
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             random_id=random.randint(0, 2 ** 64),
                                             message=f"Выберите режим",
                                             keyboard=json.dumps(menu_keyboard, ensure_ascii=False))
                        if cur.execute('''SELECT msg_flag FROM msg WHERE vk_id = ?''',
                                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
                            0] == 1:

                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             random_id=random.randint(0, 2 ** 64),
                                             message=f"Выберите игру",
                                             keyboard=json.dumps(watch_keyboard, ensure_ascii=False))
                            cur.execute('''UPDATE msg
                                                                        SET msg_flag = 0
                                                                        WHERE vk_id = ?''',
                                        ('https://vk.com/id' + str(event.obj.message['from_id']),))
                            con.commit()
                        else:

                            if cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                           ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
                                0] is None:
                                if chek_profile('https://vk.com/id' + str(event.obj.message['from_id']),
                                                "CSGO") or chek_profile(
                                    'https://vk.com/id' + str(event.obj.message['from_id']), "RL"):
                                    pass

                        if event.obj.message['text'] == 'смотреть CSGO':
                            cur.execute('''UPDATE msg
                                        SET game = ?
                                         WHERE vk_id = ?''',
                                        ('csgo', 'https://vk.com/id' + str(event.obj.message['from_id']),))
                            cur.execute('''UPDATE msg
                                            SET msg_flag = 0
                                            WHERE vk_id = ?''',
                                        ('https://vk.com/id' + str(event.obj.message['from_id']),))
                            con.commit()
                        if event.obj.message['text'] == 'смотреть RL':
                            cur.execute('''UPDATE msg
                                                                    SET game = ?
                                                                    WHERE vk_id = ?''',
                                        ('rl', 'https://vk.com/id' + str(event.obj.message['from_id']),))
                            con.commit()
                        if cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
                            0] is not None:
                            await send_profile(event, cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                                  ('https://vk.com/id' + str(
                                                                      event.obj.message['from_id']),)).fetchall()[0][0])
                            send_flag = True
                            vk_url = 'https://vk.com/id' + str(event.obj.message['from_id'])
                            for event in longpoll.listen():
                                if event.type == VkBotEventType.MESSAGE_NEW:
                                    cur.execute('''UPDATE msg
                                                       SET last_msg = ?
                                                       WHERE vk_id = ?''', (
                                        event.obj.message['text'],
                                        'https://vk.com/id' + str(event.obj.message['from_id']),))
                                    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                   (vk_url,)).fetchall()[0][0] == 'Смотреть анкеты' or \
                                            cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                        (vk_url,)).fetchall()[0][0] in setting_words:
                                        cur.execute('''UPDATE msg
                                                                                        SET watch_flag = 1
                                                                                        WHERE vk_id = ?''', (
                                            'https://vk.com/id' + str(event.obj.message['from_id']),))
                                        if cur.execute('''SELECT msg_flag FROM msg WHERE vk_id = ?''',
                                                       ('https://vk.com/id' + str(
                                                           event.obj.message['from_id']),)).fetchall()[0][
                                            0] == 1:
                                            vk.messages.send(user_id=event.obj.message['from_id'],
                                                             random_id=random.randint(0, 2 ** 64),
                                                             message=f"Выберите игру",
                                                             keyboard=json.dumps(watch_keyboard,
                                                                                 ensure_ascii=False))
                                            cur.execute('''UPDATE msg
                                                         SET msg_flag = 0
                                                        WHERE vk_id = ?''',
                                                        ('https://vk.com/id' + str(event.obj.message['from_id']),))
                                            con.commit()
                                        else:
                                            if chek_profile(
                                                    'https://vk.com/id' + str(event.obj.message['from_id']),
                                                    "CSGO") or chek_profile(
                                                'https://vk.com/id' + str(event.obj.message['from_id']),
                                                "CSGO"):
                                                pass
                                            else:
                                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                                 random_id=random.randint(0, 2 ** 64),
                                                                 message=f"Сначала зарегестрируйстесь")
                                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                                 random_id=random.randint(0, 2 ** 64),
                                                                 message=f"Выберите режим",
                                                                 keyboard=json.dumps(menu_keyboard,
                                                                                     ensure_ascii=False)
                                                                 )
                                        if event.obj.message['text'] == 'смотреть CSGO':
                                            cur.execute('''UPDATE msg
                                                                                               SET game = ?
                                                                                                WHERE vk_id = ?''',
                                                        ('csgo',
                                                         'https://vk.com/id' + str(event.obj.message['from_id']),))
                                            cur.execute('''UPDATE msg
                                                                                                   SET msg_flag = 0
                                                                                                   WHERE vk_id = ?''',
                                                        ('https://vk.com/id' + str(event.obj.message['from_id']),))
                                            con.commit()
                                        if event.obj.message['text'] == 'смотреть RL':
                                            cur.execute('''UPDATE msg
                                                          SET game = ?
                                                          WHERE vk_id = ?''',
                                                        (
                                                        'rl', 'https://vk.com/id' + str(event.obj.message['from_id']),))
                                        if cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                       ('https://vk.com/id' + str(
                                                           event.obj.message['from_id']),)).fetchall()[0][
                                            0] is not None:
                                            await send_profile(event,
                                                               cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                                           ('https://vk.com/id' + str(event.obj.message[
                                                                                                          'from_id']),)).fetchall()[
                                                                   0][0])
                                    con.commit()
                                if event.type == VkBotEventType.MESSAGE_NEW and \
                                        cur.execute('''SELECT watch_flag FROM msg WHERE vk_id = ?''',
                                                    (vk_url,)).fetchall()[0][0] == '1' and \
                                        cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                    ('https://vk.com/id' + str(
                                                        event.obj.message['from_id']),)).fetchall()[0][0] is not None:
                                    cur.execute('''UPDATE msg
                                                    SET last_msg = ?
                                                    WHERE vk_id = ?''', (
                                        event.obj.message['text'],
                                        'https://vk.com/id' + str(event.obj.message['from_id']),))
                                    txt = event.obj.message['text']
                                    try:
                                        if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                       ('https://vk.com/id' + str(
                                                           event.obj.message['from_id']),)).fetchall()[0][
                                            0] == 'Понравилось' and \
                                                cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                            ('https://vk.com/id' + str(
                                                                event.obj.message['from_id']),)).fetchall()[0][
                                                    0] is not None:
                                            await send_id(event, cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                                             ('https://vk.com/id' + str(
                                                                                 event.obj.message[
                                                                                     'from_id']),)).fetchall()[0][0])
                                            if cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',('https://vk.com/id' + str(
                                                                                 event.obj.message[
                                                                                     'from_id']),)).fetchall()[0][0] == 'csgo':
                                                cur.execute('''UPDATE csgo 
                                                                SET counter = counter + 1
                                                                WHERE vk_id = ?''',
                                                            ('https://vk.com/id' + str(
                                                                event.obj.message['from_id']),)).fetchall()
                                            elif cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                                             ('https://vk.com/id' + str(
                                                                                 event.obj.message[
                                                                                     'from_id']),)).fetchall()[0][0] == 'rl':

                                                cur.execute('''UPDATE csgo 
                                                            SET counter = counter + 1
                                                            WHERE vk_id = ?''',
                                                            ('https://vk.com/id' + str(
                                                                event.obj.message['from_id']),)).fetchall()
                                        elif cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                         ('https://vk.com/id' + str(
                                                             event.obj.message['from_id']),)).fetchall()[
                                            0][0] == 'Не понравилось' and \
                                                cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                            ('https://vk.com/id' + str(
                                                                event.obj.message['from_id']),)).fetchall()[0][
                                                    0] is not None:
                                            cur.execute('''UPDATE csgo 
                                                               SET counter = counter + 1
                                                               WHERE vk_id = ?''',
                                                        ('https://vk.com/id' + str(
                                                            event.obj.message['from_id']),)).fetchall()
                                            send_flag = True
                                        elif cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                         ('https://vk.com/id' + str(
                                                             event.obj.message['from_id']),)).fetchall()[0][
                                            0] == 'Меню режимов' and \
                                                cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                            ('https://vk.com/id' + str(
                                                                event.obj.message['from_id']),)).fetchall()[0][
                                                    0] is not None:
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
                                            cur.execute('''UPDATE msg
                                                             SET watch_flag = 0
                                                            WHERE vk_id = ?''',
                                                        ('https://vk.com/id' + str(event.obj.message['from_id']),))
                                            cur.execute('''UPDATE msg
                                                            SET game = ?
                                                            WHERE vk_id = ?''', (
                                                None, 'https://vk.com/id' + str(event.obj.message['from_id']),))
                                            cur.execute('''UPDATE msg SET msg_flag = 1 WHERE vk_id = ?''',
                                                        ('https://vk.com/id' + str(event.obj.message['from_id']),))
                                            send_flag = False
                                            con.commit()
                                    except IndexError:
                                        pass
                                    try:
                                        if send_flag:
                                            await send_profile(event,
                                                               cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                                           ('https://vk.com/id' + str(event.obj.message[
                                                                                                          'from_id']),)).fetchall()[
                                                                   0][0])
                                    except IndexError:
                                        vk.messages.send(user_id=event.obj.message['from_id'],
                                                         random_id=random.randint(0, 2 ** 64),
                                                         message=f"Анкет больше нету")
                                        cur.execute('''UPDATE csgo 
                                                            SET counter = 0
                                                            WHERE vk_id = ?''',
                                                    ('https://vk.com/id' + str(
                                                        event.obj.message['from_id']),)).fetchall()

                                    con.commit()
                                    vk_url = 'https://vk.com/id' + str(event.obj.message['from_id'])

                                elif event.type == VkBotEventType.MESSAGE_NEW:
                                    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                   (vk_url,)).fetchall()[0][0] == 'Создать свою':
                                        await game_choose(event)
                                    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                   (vk_url,)).fetchall()[0][0] == 'CSGO':
                                        cur.execute('''UPDATE csgo
                                                            SET lst_flag = 1
                                                            WHERE vk_id = ?''',
                                                    ('https://vk.com/id' + str(event.obj.message['from_id']),))
                                    elif cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                     (vk_url,)).fetchall()[0][0] == 'RL':
                                        cur.execute('''UPDATE rl
                                                    SET lst_flag = 1
                                                    WHERE vk_id = ?''',
                                                    ('https://vk.com/id' + str(event.obj.message['from_id']),))
                                    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                   (vk_url,)).fetchall()[0][0] in games:
                                        if event.obj.message['text'] == 'RL':
                                            cur.execute('''UPDATE msg
                                                            SET create_game = ?
                                                            WHERE vk_id = ?''', (
                                            'rl', 'https://vk.com/id' + str(event.obj.message['from_id']),))
                                        elif event.obj.message['text'] == 'CSGO':
                                            cur.execute('''UPDATE msg
                                                        SET create_game = ?
                                                        WHERE vk_id = ?''',
                                                        ('csgo',
                                                         'https://vk.com/id' + str(event.obj.message['from_id']),))
                                        con.commit()
                                    if cur.execute('''SELECT create_game FROM msg WHERE vk_id = ?''',
                                    ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == 'csgo':
                                        csgo(event)
                                    elif cur.execute('''SELECT create_game 
                                    FROM msg WHERE vk_id = ?''',
                                    ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == 'rl':
                                        rl(event)

                except IndexError:
                    pass
                txt = event.obj.message['text']
                cur.execute('''UPDATE msg
                                                            SET last_msg = ?
                                                            WHERE vk_id = ?''',
                            (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))

                if txt == 'Создать свою':
                    await game_choose(event)
                    cur.execute('''UPDATE msg
                                        SET msg_flag = 1
                                        WHERE vk_id = ?''',
                                ('https://vk.com/id' + str(event.obj.message['from_id']),))


                    cur.execute('''UPDATE msg
                                    SET game = ?
                                    WHERE vk_id = ?''',
                                (None, 'https://vk.com/id' + str(event.obj.message['from_id']),))
                    con.commit()
            if event.obj.message['text'] == 'RL':
                cur.execute('''UPDATE rl
                                                 SET lst_flag = 1
                                                 WHERE vk_id = ?''',
                            ('https://vk.com/id' + str(event.obj.message['from_id']),))
                cur.execute('''UPDATE msg
                                SET create_game = ?
                                WHERE vk_id = ?''', ('rl', 'https://vk.com/id' + str(event.obj.message['from_id']),))
            elif event.obj.message['text'] == 'CSGO':
                cur.execute('''UPDATE csgo
                                                 SET lst_flag = 1
                                                 WHERE vk_id = ?''',
                            ('https://vk.com/id' + str(event.obj.message['from_id']),))
                cur.execute('''UPDATE msg
                            SET create_game = ?
                            WHERE vk_id = ?''',
                            ('csgo', 'https://vk.com/id' + str(event.obj.message['from_id']),))
            try:
                if cur.execute('''SELECT create_game FROM msg WHERE vk_id = ?''',
                                    ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == 'rl':
                    rl(event)
                elif cur.execute('''SELECT create_game FROM msg WHERE vk_id = ?''',
                                    ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == 'csgo':
                    csgo(event)
            except IndexError:
                pass
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
