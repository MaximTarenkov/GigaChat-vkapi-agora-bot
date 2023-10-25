import traceback
import vk_api
import pickle
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

# авторизация бота
vk_session = vk_api.VkApi(token='')
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id='220945844')



while True: 
    
    try:
        
        def load_data(value):
            with open("social_credit.txt", "r") as f:
                social_credit = {}
                for line in f:
                    line = line.strip()
                    line = line.replace("{", "").replace("}", "")
                    user_id, mentioned_id = line.split(":")
                    user_id = int(user_id)
                    mentioned_id = float(mentioned_id)
                    if value == 'user_id':
                        return user_id
                    if value == 'mentioned_id':
                        return mentioned_id
        

        user_id = load_data('user_id')
        mentioned_id = load_data('mentioned_id')
        social_credit = {user_id: mentioned_id}

        
        # функция сохранения всех необходимых данных в txt файл
        def save_data(mentioned_id, social_credit, log_type, filename):
            if log_type == 'log':
                with open(filename, "a") as f:
                    f.write("\n")
                    f.write(str(mentioned_id))
                    f.write(" ")
                    f.write(str(social_credit[mentioned_id]))
            if log_type == 'data_save':
                with open(filename, 'w') as f:
                    f.write(str(social_credit))

        # функция для подсчёта ск
        def calculate_y(x):
            if x >= 1000:
                y = ((x - 1000) ** 2) / 100000
            else:
                y = -((x - 1000) ** 2) / 100000
            if y == 0:
                y = 0.1
            return y
        
        def readLogCommand(filename): # что это, я не помню вообще
            if message.startswith(f'Read log') or message.startswith(f'read log'):
                with open (filename, 'r') as f:
                    log = f.readlines()
                    #line_log = str(count_lines('social_credit.txt'))
                    #mess = log
                    vk.messages.send(
                            chat_id = event.chat_id,
                            message = log,
                            random_id = get_random_id()
                        )
                    
        # цикл для подключени к серверу longpoll
        # это нужно для получения данных о новых сообщениях
        # каждый цикл проверяет чат на наличие новых событий
        for event in longpoll.listen():
            print(social_credit) # вывод всех данных, что находятся в social_credit для дебага
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:

                # инициализация нового сообщения, которое появилось в чате
                # и кем оно было отправлено
                message = event.message['text']
                user_id = event.message['from_id']

                # проверка на отправку сообщения не сообществом (ботом)
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and not event.message['from_id'] < 0:

                    # начисление 1000 начального рейтинга, если его нет в social_credit
                    if user_id not in social_credit:
                        social_credit[user_id] = 1000

                    # обработка сообщений 
                    if message.startswith(f'+'): # обработка сообщений, которые начинаются на +
                        # инициализация переменной, определяющей к-во ск
                        countSR = 15
                        countSR = int(message.strip("+").strip()[0::].strip("ск")) # получение данных о к-во ск
                        # получение id упомянутого юзера
                        mentioned_id = event.message['reply_message']['from_id']

                        # подсчёт ск (в будущем нужно поместить это ещё в одну функцию для большей читабельности кода)
                        x = social_credit[mentioned_id]
                        y = calculate_y(x)
                        new_sc = countSR / y

                        #присваивание рейтинга
                        social_credit[mentioned_id] += new_sc

                        # вывод сообщения об изменении социального рейтинга
                        vk.messages.send(
                            chat_id = event.chat_id,
                            message = f'Добавлено {new_sc} очков социального рейтинга.\nВсего: {round(social_credit[mentioned_id])}',
                            random_id = get_random_id()
                        )
                        
                        # сохранение данных о пользователях и логгирование
                        save_data(mentioned_id, social_credit, 'log', "social_credit_log.txt")
                        save_data(mentioned_id, social_credit, 'data_save', "social_credit.txt")
                    

                
    except Exception as e: # в случае возвращения ошибки отсчёт об ней в чат
        vk.messages.send(
            chat_id = event.chat_id,
            message = f'{e}\n{traceback.format_exc()}',
            random_id = get_random_id()
        )

    continue
