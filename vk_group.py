import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import datetime
import json
import sqlite3

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
        ]
    ]
}
menu_keyboard = {
    "one_time": True,
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


def main():
    vk_session = vk_api.VkApi(
        token='5a8ec1e58a79d88b952ee899071f2a021fbcb656497358cbdec9143044f8d5e5410f9fa2a71fd001486bf')

    longpoll = VkBotLongPoll(vk_session, '193164016')
    comand_lst = ['!статус', '!Россия']
    key_words = ['PUBG', 'Fortnite', 'Dota 2', 'CSGO', 'Ранг', 'Кол-во часов', 'Ссылка на стр вк', ]
    setting_words = ['Смотреть анкеты', 'Создать свою']
    csgo_rangs = ['Сильвер', 'Звёзды', 'Калаши', 'Бигастар - Лем', 'Суприм - Глобал']
    csgo_hours = ["100-300", "300-500", "500-800", "800-1000", "1500"]
    rang_csgo_flag = False
    csgo_flag = True
    lst_flag = False
    menu_flag = True
    con = sqlite3.connect('db/csgo.sqlite3')
    cur = con.cursor()
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            vk = vk_session.get_api()
            txt = event.obj.message['text']
            vk_url = 'https://vk.com/id' + str(event.obj.message['from_id'])
            rank = ''
            if event.obj.message['text'] not in comand_lst and txt not in key_words:
                if menu_flag:
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     message=f"Выберите режим",
                                     keyboard=json.dumps(menu_keyboard, ensure_ascii=False)
                                     )
                    menu_flag = False
                user_id = event.obj.message['from_id']
                if event.obj.message['text'] == 'Смотреть анкеты':

                    profiles = cur.execute('''SELECT * from csgo  WHERE vk_id is not Null''').fetchall()
                    stroka = f"Ранг - {profiles[cur.execute('''SELECT counter from csgo WHERE vk_id = ?''', (vk_url,)).fetchall()[0][0]][1]}, Колличество часов - {profiles[cur.execute('''SELECT counter from csgo WHERE vk_id = ?''', (vk_url,)).fetchall()[0][0]][2]}"
                    vk.messages.send(user_id=user_id,
                                     random_id=random.randint(0, 2 ** 64),
                                     message=stroka,
                                     keyboard=json.dumps(like_keyboard, ensure_ascii=False))

                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW:
                            vk_url = 'https://vk.com/id' + str(event.obj.message['from_id'])
                            cur.execute('''UPDATE csgo
                                        SET last_msg = ?
                                        WHERE vk_id = ?''', (event.obj.message['text'], vk_url,))
                            counter = \
                            cur.execute('''SELECT counter from csgo WHERE vk_id = ?''', (vk_url,)).fetchall()[0][0]
                            print(counter)
                            txt = event.obj.message['text']
                            print(cur.execute('''SELECT last_msg FROM csgo WHERE vk_id = ?''', (vk_url,)).fetchall())
                            try:
                                if cur.execute('''SELECT last_msg FROM csgo WHERE vk_id = ?''', (vk_url,)).fetchall()[0][0] == 'Понравилось':
                                    vk.messages.send(user_id=event.obj.message['from_id'],
                                                     random_id=random.randint(0, 2 ** 64),
                                                     message=f"Профиль игрока - {profiles[cur.execute('''SELECT counter from csgo WHERE vk_id = ?''', (vk_url,)).fetchall()[0][0]][0]}")
                                    cur.execute('''UPDATE csgo 
                                                SET counter = counter + 1
                                                WHERE vk_id = ?''', (vk_url,)).fetchall()
                                    counter = \
                                        cur.execute('''SELECT counter from csgo WHERE vk_id = ?''',
                                                    (vk_url,)).fetchall()[
                                            0][0]
                                    print(counter)
                                elif cur.execute('''SELECT last_msg FROM csgo WHERE vk_id = ?''', (vk_url,)).fetchall()[0][0] == 'Не понравилось':
                                    cur.execute('''UPDATE csgo 
                                                   SET counter = counter + 1
                                                   WHERE vk_id = ?''', (vk_url,)).fetchall()
                                    counter = cur.execute('''SELECT counter from csgo WHERE vk_id = ?''', (vk_url,)).fetchall()[0][0]
                                    print(counter)
                            except IndexError:
                                pass
                            try:
                                stroka = f"Ранг - {profiles[counter][1]}, Колличество часов - {profiles[cur.execute('''SELECT counter from csgo WHERE vk_id = ?''', (vk_url,)).fetchall()[0][0]][2]}"
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 random_id=random.randint(0, 2 ** 64),
                                                 message=stroka,
                                                 keyboard=json.dumps(like_keyboard, ensure_ascii=False))
                            except IndexError:
                                vk.messages.send(user_id=event.obj.message['from_id'],
                                                 random_id=random.randint(0, 2 ** 64),
                                                 message=f"Анкет больше нету")
                                cur.execute('''UPDATE csgo 
                                                SET counter = 0
                                                WHERE vk_id = ?''',
                                            (vk_url,)).fetchall()

                            con.commit()

                if txt == 'Создать свою':
                    vk.messages.send(user_id=event.obj.message['from_id'],
                                     random_id=random.randint(0, 2 ** 64),
                                     message=f"Выберите игру:",
                                     keyboard=json.dumps(keyboard, ensure_ascii=False))
                    lst_flag = True

            if event.obj.message['text'] == '!статус':
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message="Пока что пользуетесь ботом через лс",
                                 random_id=random.randint(0, 2 ** 64))
            elif event.obj.message['text'] == 'CSGO' and lst_flag:
                try:
                    result = cur.execute('''INSERT INTO csgo(vk_id, counter) 
                                            VALUES(?, ?)''', (vk_url, 0,))
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
                    print(csgo_flag)
                print(csgo_flag)
                if csgo_flag:
                    print(csgo_flag)
                    for event in longpoll.listen():
                        if event.type == VkBotEventType.MESSAGE_NEW:
                            txt = event.obj.message['text']
                            print(txt)
                            if event.obj.message['text'] == 'Ранг' and csgo_flag:
                                if len(vk_url) == 0:
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
                                                        WHERE vk_id = ?''', (txt, vk_url,))
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
                                                        WHERE vk_id = ?''', (txt, vk_url,))
                                con.commit()


if __name__ == '__main__':
    main()
