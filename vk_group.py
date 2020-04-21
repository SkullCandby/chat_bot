import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import datetime
import json
import sqlite3
import asyncio

'''
пояснение к переменным таблицы.
сsgo:
csgo_flag - этот флаг я использую в процессе создания анкеты
lst_flag - флаг для отправки сообщений
vk_id - id пользователся
rank - ранк пользователя
hours - кол-во часов 
rl:
csgo_flag - этот флаг я использую в процессе создания анкеты, проверка того можно ли создавать анкету
lst_flag - флаг для отправки сообщений
vk_id - id пользователся
rank - ранк пользователя
hours - кол-во часов
msg:
last_msg - последние сообщение пользователя
vk_id - id пользовтеля
watch_flag - если флаг равен 1, то пользователь может смотреть анкеты, если нет, то нет
game - это игра которую смотрит человек
msg_flag - флаг для отправки сообщений
create_game - игра по которой я создаю анкету
counter - это обычный счётчик для просмотра анкет
csgo - это таблица в которой хранятся данные пользователей котрые зарегестрировались в csgo
rl - это таблица в которой хранятся данные пользователей котрые зарегестрировались в rl
msg - в этой таблице хранятся данные которыми пользователей пользуются и в случае когда он создаёт или смотрит анкету/
анкеты csgo и в случае с rl. тут хранятся последнии сооьщения, счётчик и тд.
'''
vk_session = vk_api.VkApi(
    token='9ee8528a5486ff195b298ba1a30994c98def107c137d8a2a058c26df9127c21487f7843bb399e51d9fd08')

longpoll = VkBotLongPoll(vk_session, '193164016')
# Ниже это 'ключевые' слова для проверки некоторых условий
comand_lst = ['!статус', '!Россия']
create_profile_words = ['RL', 'Fortnite', 'Dota 2', 'CSGO', 'Ранг', 'Кол-во часов', 'Ссылка на стр вк', "100-500",
                        "500-800", "800-1000", "1000-1500", "1500+", 'Сильвер 1', 'Сильвер 2', 'Сильвер 3', 'Сильвер 4',
                        'Сильвер 5', 'Сильвер 6', 'Звёзда 1', 'Звёзда 2', 'Звёзда 3', 'Звёзда 4', 'Калаш',
                        'Калаш с винками', 'Два калаша', 'Бигстар',
                        'Беркут', 'Лем', 'Суприм', 'Глобал', 'Prospect 1 - Prospect elite',
                        'challenger 1 - challenger elite',
                        'rising star - champion']
games = ['RL', 'Fortnite', 'Dota 2', 'CSGO']
like_words = ['Понравилось', 'Не понравилось']
setting_words = ['смотреть CSGO', 'смотреть RL']
csgo_rangs = ['Сильвер 1', 'Сильвер 2', 'Сильвер 3', 'Сильвер 4', 'Сильвер 5', 'Сильвер 6', 'Звёзда 1', 'Звёзда 2',
              'Звёзда 3', 'Звёзда 4', 'Калаш', 'Калаш с винками', 'Два калаша', 'Бигстар',
              'Беркут', 'Лем', 'Суприм', 'Глобал']
hours = ["100-500", "500-800", "800-1000", '1000-1500', "1500+"]
rl_rangs = ['Prospect 1 - Prospect elite', 'challenger 1 - challenger elite', 'rising star - champion']
vk = vk_session.get_api()
con = sqlite3.connect('db/csgo.sqlite3')
cur = con.cursor()
# Создаваю клавиатуры
like_keyboard = VkKeyboard(one_time=False)
like_keyboard.add_button('Понравилось', color=VkKeyboardColor.PRIMARY)
like_keyboard.add_button('Не понравилось', color=VkKeyboardColor.NEGATIVE)
like_keyboard.add_button('Меню режимов', color=VkKeyboardColor.POSITIVE)

menu_keyboard = VkKeyboard(one_time=False)
menu_keyboard.add_button('Смотреть анкеты', color=VkKeyboardColor.PRIMARY)
menu_keyboard.add_button('Создать свою', color=VkKeyboardColor.NEGATIVE)

keyboard = VkKeyboard(one_time=False)
keyboard.add_button('CSGO', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('RL', color=VkKeyboardColor.NEGATIVE)

csgo_keyboard = VkKeyboard(one_time=False)
csgo_keyboard.add_button('Ранг', color=VkKeyboardColor.PRIMARY)
csgo_keyboard.add_button('Кол-во часов', color=VkKeyboardColor.NEGATIVE)

hours_keyboard = VkKeyboard(one_time=False)
hours_keyboard.add_button('100-500', color=VkKeyboardColor.PRIMARY)
hours_keyboard.add_line()
hours_keyboard.add_button('500-800', color=VkKeyboardColor.PRIMARY)
hours_keyboard.add_button('800-1000', color=VkKeyboardColor.NEGATIVE)
hours_keyboard.add_button('1000-1500', color=VkKeyboardColor.PRIMARY)
hours_keyboard.add_line()
hours_keyboard.add_button('1500+', color=VkKeyboardColor.NEGATIVE)

csgo_rang_keyboard = VkKeyboard(one_time=False)
csgo_rang_keyboard.add_button('Сильвер 1', color=VkKeyboardColor.PRIMARY)
csgo_rang_keyboard.add_button('Сильвер 2', color=VkKeyboardColor.PRIMARY)
csgo_rang_keyboard.add_button('Сильвер 3', color=VkKeyboardColor.PRIMARY)
csgo_rang_keyboard.add_line()
csgo_rang_keyboard.add_button('Сильвер 4', color=VkKeyboardColor.PRIMARY)
csgo_rang_keyboard.add_button('Сильвер 5', color=VkKeyboardColor.PRIMARY)
csgo_rang_keyboard.add_button('Сильвер 6', color=VkKeyboardColor.PRIMARY)
csgo_rang_keyboard.add_line()
csgo_rang_keyboard.add_button('Звёзда 1', color=VkKeyboardColor.NEGATIVE)
csgo_rang_keyboard.add_button('Звёзда 2', color=VkKeyboardColor.NEGATIVE)
csgo_rang_keyboard.add_button('Звёзда 3', color=VkKeyboardColor.NEGATIVE)
csgo_rang_keyboard.add_button('Звёзда 4', color=VkKeyboardColor.NEGATIVE)
csgo_rang_keyboard.add_line()
csgo_rang_keyboard.add_button('Калаш', color=VkKeyboardColor.PRIMARY)
csgo_rang_keyboard.add_button('Калаш с винками', color=VkKeyboardColor.PRIMARY)
csgo_rang_keyboard.add_button('Два калаша', color=VkKeyboardColor.PRIMARY)
csgo_rang_keyboard.add_line()
csgo_rang_keyboard.add_button('Бигстар', color=VkKeyboardColor.NEGATIVE)
csgo_rang_keyboard.add_button('Беркут', color=VkKeyboardColor.NEGATIVE)
csgo_rang_keyboard.add_button('Лем', color=VkKeyboardColor.NEGATIVE)
csgo_rang_keyboard.add_line()
csgo_rang_keyboard.add_button('Суприм', color=VkKeyboardColor.PRIMARY)
csgo_rang_keyboard.add_button('Глобал', color=VkKeyboardColor.PRIMARY)

watch_keyboard = VkKeyboard(one_time=False)
watch_keyboard.add_button('смотреть CSGO', color=VkKeyboardColor.PRIMARY)
watch_keyboard.add_button('смотреть RL', color=VkKeyboardColor.NEGATIVE)

rl_rangs_keyboard = VkKeyboard(one_time=False)
rl_rangs_keyboard.add_button('Prospect 1 - Prospect elite', color=VkKeyboardColor.PRIMARY)
rl_rangs_keyboard.add_button('challenger 1 - challenger elite', color=VkKeyboardColor.NEGATIVE)
rl_rangs_keyboard.add_button('rising star - champion', color=VkKeyboardColor.POSITIVE)


def chek_profile(vk_id, game=None):
    # это функия для проверки полностью ли пользователь заполнил анкету
    if game == 'CSGO':
        # это переменную я не засовывал в бд потому что я пользуюсь не постояно
        flag = True
        try:
            # получаю список пользователя со всеми параметрами
            profiles = cur.execute('''SELECT * from csgo WHERE vk_id = ?''', (vk_id,)).fetchall()[0]
            for i in range(len(profiles)):
                # бегу по списку и если парамер не заполнен то есть None флаг утсанавливаю его на False
                if profiles[i] is None:
                    flag = flag and False
        except IndexError:
            flag = False
        return flag
    elif game == 'rl':
        # здесь тоже самое, но для другой игры
        flag = True
        try:
            profiles = cur.execute('''SELECT * from rl WHERE vk_id = ?''', (vk_id,)).fetchall()[0]
            for i in range(len(profiles)):
                if profiles[i] is None:
                    flag = flag and False
        except IndexError:
            flag = False
        return flag


async def send_msg(event):
    # это функция для отправки выбора режима, она как бы и ничего не делает
    # особенного, поэтому смысла не было делать эту функцию, но я сделал чтобы хоть как-то сократить код
    vk.messages.send(user_id=event.obj.from_id,
                     random_id=random.randint(0, 2 ** 64),
                     message=f"Выберите режим",
                     keyboard=menu_keyboard.get_keyboard())


async def send_profile(event, game):
    # функция для отправки профиля пользователя
    if game == 'csgo':
        # получаю его характеристики
        profiles = cur.execute('''SELECT * from csgo  WHERE vk_id is not Null''').fetchall()
        # формирую строку в который будут написаны характеристики пользователся
        stroka = f"Ранг - {profiles[cur.execute('''SELECT counter from msg WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][1]}, Колличество часов - {profiles[cur.execute('''SELECT counter from msg WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][2]}"
        # отпраляю сообщение
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=stroka,
                         keyboard=like_keyboard.get_keyboard())
    elif game == 'rl':
        # здесь тоже самое
        profiles = cur.execute('''SELECT * from rl  WHERE vk_id is not Null''').fetchall()
        stroka = f"Ранг - {profiles[cur.execute('''SELECT counter from msg WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][1]}, Колличество часов - {profiles[cur.execute('''SELECT counter from msg WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][2]}"
        # отпраляю сообщение
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=stroka,
                         keyboard=like_keyboard.get_keyboard())
    # устанавливаю msg_flag на 1
    cur.execute('''UPDATE msg SET msg_flag = 1 WHERE vk_id = ?''',
                ('https://vk.com/id' + str(event.obj.message['from_id']),))


async def game_choose(event):
    # сообщение для выбора игры, в некоторых случаях event.obj.message - None поэтому
    # приходится добовлять  такие условия
    # ниже я просто отправляю сообщения
    if event.obj.message is None:
        vk.messages.send(user_id=event.obj['peer_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите игру:",
                         keyboard=keyboard.get_keyboard())
    else:
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите игру:",
                         keyboard=keyboard.get_keyboard())


async def send_id(event, game):
    # функция для отправки профиля в случае если пользователю понравилась анкеты другого пользователя
    if game == 'csgo':
        # опять получаю характеристики  пользователя
        profiles = cur.execute('''SELECT * from csgo  WHERE vk_id is not Null''').fetchall()
        # получаю id пользователя который понравился другому пользователю
        profile = profiles[cur.execute('''SELECT counter from msg WHERE vk_id = ?''',
                                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][0]
        # отправка сообзения
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f'Профиль игрока: {profile}',
                         keyboard=like_keyboard.get_keyboard())
        # устанавливаю msg_flag на 1
        cur.execute('''UPDATE msg SET msg_flag = 1 WHERE vk_id = ?''',
                    ('https://vk.com/id' + str(event.obj.message['from_id']),))
    elif game == 'rl':
        # тут тоже самое
        profiles = cur.execute('''SELECT * from rl  WHERE vk_id is not Null''').fetchall()
        profile = profiles[cur.execute('''SELECT counter from msg WHERE vk_id = ?''',
                                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0]][0]
        # отправка сообзения
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f'Профиль игрока: {profile}',
                         keyboard=like_keyboard.get_keyboard())
        # устанавливаю msg_flag на 1
        cur.execute('''UPDATE msg SET msg_flag = 1 WHERE vk_id = ?''',
                    ('https://vk.com/id' + str(event.obj.message['from_id']),))

def csgo_profile(event):
    # эта фунция для создания анкеты
    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == 'Ранг' and cur.execute('''SELECT csgo_flag FROM csgo WHERE vk_id = ?''',
                                     ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == '1':
        # сообщение с выбором ранга

        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите ранг",
                         keyboard=csgo_rang_keyboard.get_keyboard())
    if event.obj.message['text'] in csgo_rangs and cur.execute('''SELECT csgo_flag FROM csgo WHERE vk_id = ?''', (
            'https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == '1':
        cur.execute('''UPDATE csgo
                                        SET rank = ?
                                        WHERE vk_id = ?''',
                    (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message='Колличество часов',
                         keyboard=hours_keyboard.get_keyboard())

        con.commit()
    if event.obj.message['text'] == 'Кол-во часов' and cur.execute('''SELECT csgo_flag FROM csgo WHERE vk_id = ?''',
                                                                   ('https://vk.com/id' + str(event.obj.message[
                                                                                                  'from_id']),)).fetchall()[
        0][0] == '1':
        # я выбираю характеристики последовательно, чтобы после выбора ранга, выходить в меню
        if cur.execute('''SELECT rank FROM csgo WHERE vk_id = ?''',
                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] is not None:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message='Выберите кол-во часов',
                             keyboard=hours_keyboard.get_keyboard())
        else:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message='Сначала скажите свой ранг')
            vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message='Ранг',
                             keyboard=csgo_rang_keyboard.get_keyboard())
    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] in hours:
        cur.execute('''UPDATE csgo
                        SET hours = ?
                        WHERE vk_id = ?''',
                    (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))
    if chek_profile('https://vk.com/id' + str(event.obj.message['from_id']), "CSGO"):
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите режим",
                         keyboard=menu_keyboard.get_keyboard())

        cur.execute('''UPDATE msg
                        SET create_game = ?
                        WHERE vk_id = ?''',
                    (None, 'https://vk.com/id' + str(event.obj.message['from_id']),))
        con.commit()


def csgo(event):
    # обновляю последние сообщение
    cur.execute('''UPDATE msg
                SET last_msg = ?
                WHERE vk_id = ?''', (
        event.obj.message['text'],
        'https://vk.com/id' + str(event.obj.message['from_id']),))
    try:
        # вставляю значени для пользователя
        cur.execute('''INSERT INTO csgo(vk_id, csgo_flag, lst_flag) VALUES(?, 1, 1)''',
                    ('https://vk.com/id' + str(event.obj.message['from_id']),))
        con.commit()
    except sqlite3.IntegrityError:
        # если такой пользователь уже есть то сообщаю об этом
        if chek_profile('https://vk.com/id' + str(event.obj.message['from_id'])):
            vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message='Такой пользоватьель уже есть',
                             keyboard=menu_keyboard.get_keyboard())
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
                         keyboard=csgo_keyboard.get_keyboard())
        # устанавливаю флаг на 0 потому что инфармационное сообщение я отправлять уже не буду
        cur.execute('''UPDATE csgo
                        SET lst_flag = 0
                        WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),))

    if cur.execute('''SELECT csgo_flag FROM csgo WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == '1':
        txt = event.obj.message['text']
        csgo_profile(event)


def rl(event):
    # тоже самое что и в фунции csgo
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
                             keyboard=menu_keyboard.get_keyboard())
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
                         keyboard=csgo_keyboard.get_keyboard())
        cur.execute('''UPDATE rl
                        SET lst_flag = 0
                        WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),))
    if cur.execute('''SELECT rl_flag FROM rl WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == 1:
        txt = event.obj.message['text']
        rl_profile(event)


def rl_profile(event):
    # тоже самое что и в фунции csgo_profile
    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == 'Ранг' and cur.execute('''SELECT rl_flag FROM rl WHERE vk_id = ?''',
                                     ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] == 1:
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите ранг",
                         keyboard=rl_rangs_keyboard.get_keyboard())
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
                         keyboard=hours_keyboard.get_keyboard())
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
                             keyboard=hours_keyboard.get_keyboard())
        else:
            vk.messages.send(user_id=event.obj.message['from_id'],
                             random_id=random.randint(0, 2 ** 64),
                             message='Сначала скажите свой ранг')
    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
        0] in hours:
        cur.execute('''UPDATE rl
                        SET hours = ?
                        WHERE vk_id = ?''',
                    (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))
    if chek_profile('https://vk.com/id' + str(event.obj.message['from_id']), "rl"):
        vk.messages.send(user_id=event.obj.message['from_id'],
                         random_id=random.randint(0, 2 ** 64),
                         message=f"Выберите режим",
                         keyboard=menu_keyboard.get_keyboard())
        cur.execute('''UPDATE msg
                                SET create_game = ?
                                WHERE vk_id = ?''',
                    (None, 'https://vk.com/id' + str(event.obj.message['from_id']),))
        con.commit()


async def main():
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_TYPING_STATE:
            await send_msg(event)

        if event.type == VkBotEventType.MESSAGE_NEW:
            try:
                # вставляю характеристики
                cur.execute('''INSERT INTO msg(vk_id, last_msg, counter) 
                                                VALUES(?, ?, 0)''',
                            ('https://vk.com/id' + str(event.obj.message['from_id']), event.obj.message['text'],))

            except sqlite3.IntegrityError:
                # если такой пользователь уже есть то просто обновляем последнее сообщение
                cur.execute('''UPDATE msg
                            SET last_msg = ?
                            WHERE vk_id = ?''',
                            (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))
            con.commit()
            txt = event.obj.message['text']
            # если слово в этих списках то я прохожу мимо этого условия и цикла регистрии в часть создания анкеты
            if txt not in comand_lst and txt not in like_words and txt not in create_profile_words or txt in setting_words:
                try:
                    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                   ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][0] == \
                            'Смотреть анкеты' or txt in setting_words:
                        # устанавливаю watch_flag на 1 для просмотра анкет
                        cur.execute('''UPDATE msg
                                        SET watch_flag = 1
                                        WHERE vk_id = ?''', ('https://vk.com/id' + str(event.obj.message['from_id']),))
                        if cur.execute('''SELECT msg_flag FROM msg WHERE vk_id = ?''',
                                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
                            0] is None:
                            # если пользователь не зарегтсьрирован отправляю его на регистрацию
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             random_id=random.randint(0, 2 ** 64),
                                             message=f"Сначала зарегестрируйстесь")
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             random_id=random.randint(0, 2 ** 64),
                                             message=f"Выберите режим",
                                             keyboard=menu_keyboard.get_keyboard())
                        if cur.execute('''SELECT msg_flag FROM msg WHERE vk_id = ?''',
                                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
                            0] == 1:
                            vk.messages.send(user_id=event.obj.message['from_id'],
                                             random_id=random.randint(0, 2 ** 64),
                                             message=f"Выберите игру",
                                             keyboard=watch_keyboard.get_keyboard())
                            cur.execute('''UPDATE msg
                                                                        SET msg_flag = 0
                                                                        WHERE vk_id = ?''',
                                        ('https://vk.com/id' + str(event.obj.message['from_id']),))
                            con.commit()
                        # ниже я выставляю игры которые буду смотреть
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
                        # если пользователь не выьрал игру или написал что-то некокртно, то он не сможет смотреть анкеты
                        if cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                       ('https://vk.com/id' + str(event.obj.message['from_id']),)).fetchall()[0][
                            0] is not None:
                            # сразу отправляю анкету игрока
                            try:
                                await send_profile(event, cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                                      ('https://vk.com/id' + str(
                                                                          event.obj.message['from_id']),)).fetchall()[0][0])
                            except TypeError:
                                await send_profile(event, cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                                ('https://vk.com/id' + str(
                                                                    event.obj.from_id),)).fetchall()[0][0])
                            send_flag = True
                            vk_url = 'https://vk.com/id' + str(event.obj.message['from_id'])
                            for event in longpoll.listen():
                                if event.type == VkBotEventType.MESSAGE_NEW:
                                    # при каждом проходе по циклу обновляю последнее сообщение
                                    cur.execute('''UPDATE msg
                                                       SET last_msg = ?
                                                       WHERE vk_id = ?''', (
                                        event.obj.message['text'],
                                        'https://vk.com/id' + str(event.obj.message['from_id']),))
                                    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                   (vk_url,)).fetchall()[0][0] == 'Смотреть анкеты' or \
                                            cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                        (vk_url,)).fetchall()[0][0] in setting_words:
                                        # в этом цикле пользователь может пойти и создать свою анкету и тогда watch_flag
                                        # выстанавливается на 0, но если он опять захочет смотреть анкеты, watch_flag
                                        # будет равен 1
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
                                                             keyboard=watch_keyboard.get_keyboard())
                                            # здесь я выставляю msg_flag на ноль чтобы он больше не отправлял это
                                            # сообщение
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
                                                                 keyboard=menu_keyboard.get_keyboard())
                                        # повторяю процедуру которая была до цикла
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
                                                            'rl',
                                                            'https://vk.com/id' + str(event.obj.message['from_id']),))
                                        if cur.execute('''SELECT game FROM msg WHERE vk_id = ?''',
                                                       ('https://vk.com/id' + str(
                                                           event.obj.message['from_id']),)).fetchall()[0][
                                            0] is not None:
                                            # если  пользоваьель выбрал игру тогда ему отправляется анкеты игрока
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
                                    # обновляю последнее сообщение
                                    cur.execute('''UPDATE msg
                                                    SET last_msg = ?
                                                    WHERE vk_id = ?''', (
                                        event.obj.message['text'],
                                        'https://vk.com/id' + str(event.obj.message['from_id']),))
                                    txt = event.obj.message['text']
                                    # в этой часте кода я обрабатываю реакцию пользователя
                                    try:
                                        # обработка исключений
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
                                            cur.execute('''UPDATE msg 
                                                                                               SET counter = counter + 1
                                                                                               WHERE vk_id = ?''',
                                                        ('https://vk.com/id' + str(
                                                            event.obj.message['from_id']),)).fetchall()
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
                                            cur.execute('''UPDATE msg 
                                                                                               SET counter = counter + 1
                                                                                               WHERE vk_id = ?''',
                                                        ('https://vk.com/id' + str(
                                                            event.obj.message['from_id']),)).fetchall()
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
                                                             keyboard=menu_keyboard.get_keyboard())
                                            cur.execute('''UPDATE msg 
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
                                        cur.execute('''UPDATE msg 
                                                            SET counter = 0
                                                            WHERE vk_id = ?''',
                                                    ('https://vk.com/id' + str(
                                                        event.obj.message['from_id']),)).fetchall()

                                    con.commit()
                                    vk_url = 'https://vk.com/id' + str(event.obj.message['from_id'])

                                elif event.type == VkBotEventType.MESSAGE_NEW:
                                    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                   (vk_url,)).fetchall()[0][0] == 'Создать свою':
                                        # выбор игры
                                        await game_choose(event)
                                    # выставляю lst_flag`и для разных игор
                                    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                   (vk_url,)).fetchall()[0][0] == 'CSGO':
                                        # устанавливаю ранг и часы на None чтобы пользователь смог снова внести свои данные
                                        cur.execute('''UPDATE csgo
                                                                                           SET rank = ?
                                                                                           WHERE vk_id = ?''',
                                                    (None,
                                                     'https://vk.com/id' + str(event.obj.message['from_id']),))
                                        cur.execute('''UPDATE csgo
                                                                           SET hours = ?
                                                                           WHERE vk_id = ?''',
                                                    (None, 'https://vk.com/id' + str(event.obj.message['from_id']),))
                                        cur.execute('''UPDATE csgo
                                                            SET lst_flag = 1
                                                            WHERE vk_id = ?''',
                                                    ('https://vk.com/id' + str(event.obj.message['from_id']),))
                                    elif cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                     (vk_url,)).fetchall()[0][0] == 'RL':
                                        cur.execute('''UPDATE rl
                                                      SET rank = ?
                                                      WHERE vk_id = ?''',
                                                    (event.obj.message['text'],
                                                     'https://vk.com/id' + str(event.obj.message['from_id']),))
                                        cur.execute('''UPDATE rl
                                                      SET hours = ?
                                                      WHERE vk_id = ?''',
                                                    (None, 'https://vk.com/id' + str(event.obj.message['from_id']),))
                                        cur.execute('''UPDATE rl
                                                    SET lst_flag = 1
                                                    WHERE vk_id = ?''',
                                                    ('https://vk.com/id' + str(event.obj.message['from_id']),))
                                    if cur.execute('''SELECT last_msg FROM msg WHERE vk_id = ?''',
                                                   (vk_url,)).fetchall()[0][0] in games:
                                        if event.obj.message['text'] == 'RL':
                                            # устанавливаю ранг и часы на None чтобы пользователь смог снова внести
                                            # свои данные
                                            cur.execute('''UPDATE rl
                                                                           SET rank = ?
                                                                           WHERE vk_id = ?''',
                                                        (None,
                                                         'https://vk.com/id' + str(event.obj.message['from_id']),))
                                            cur.execute('''UPDATE rl
                                                                          SET hours = ?
                                                                          WHERE vk_id = ?''',
                                                        (
                                                            None,
                                                            'https://vk.com/id' + str(event.obj.message['from_id']),))
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
                                    # выставляем create_game
                                    if cur.execute('''SELECT create_game FROM msg WHERE vk_id = ?''',
                                                   ('https://vk.com/id' + str(
                                                       event.obj.message['from_id']),)).fetchall()[0][0] == 'csgo':
                                        csgo(event)
                                    elif cur.execute('''SELECT create_game 
                                    FROM msg WHERE vk_id = ?''',
                                                     ('https://vk.com/id' + str(
                                                         event.obj.message['from_id']),)).fetchall()[0][0] == 'rl':
                                        rl(event)

                except IndexError:
                    pass
                txt = event.obj.message['text']
                cur.execute('''UPDATE msg
                                                            SET last_msg = ?
                                                            WHERE vk_id = ?''',
                            (event.obj.message['text'], 'https://vk.com/id' + str(event.obj.message['from_id']),))
                # тут такой же процесс регистрации как и выше
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
                # устанавливаю ранг и часы на None чтобы пользователь смог снова внести свои данные
                cur.execute('''UPDATE rl
                               SET rank = ?
                               WHERE vk_id = ?''',
                            (None,
                             'https://vk.com/id' + str(event.obj.message['from_id']),))
                cur.execute('''UPDATE rl
                              SET hours = ?
                              WHERE vk_id = ?''',
                            (None, 'https://vk.com/id' + str(event.obj.message['from_id']),))
                cur.execute('''UPDATE rl
                            SET lst_flag = 1
                            WHERE vk_id = ?''',
                            ('https://vk.com/id' + str(event.obj.message['from_id']),))
                cur.execute('''UPDATE msg
                                SET create_game = ?
                                WHERE vk_id = ?''', ('rl', 'https://vk.com/id' + str(event.obj.message['from_id']),))
            elif event.obj.message['text'] == 'CSGO':
                # устанавливаю ранг и часы на None чтобы пользователь смог снова внести свои данные
                cur.execute('''UPDATE csgo
                              SET rank = ?
                              WHERE vk_id = ?''',
                            (None,
                             'https://vk.com/id' + str(event.obj.message['from_id']),))
                cur.execute('''UPDATE csgo
                              SET hours = ?
                               WHERE vk_id = ?''',
                            (None, 'https://vk.com/id' + str(event.obj.message['from_id']),))
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
