import traceback
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id

# авторизация бота
vk_session = vk_api.VkApi(token='token')
vk = vk_session.get_api()
longpoll = VkBotLongPoll(vk_session, group_id='220945844')

while True: 

    try:

        social_credit = {}

        for event in longpoll.listen():

            if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat:

                # get id message и текст
                message = event.message['text']
                user_id = event.message['from_id']
                countSR = 15

                # проверка на отправку сообщения не ботом
                if event.type == VkBotEventType.MESSAGE_NEW and event.from_chat and not event.message['from_id'] < 0:

                    # начисление юзеру 1000 начального рейтинга, если его нет в social_credit
                    if user_id not in social_credit:
                        social_credit[user_id] = 1000

                    # обработка сообщений
                    if message.startswith(f'+{countSR} ск'):

                        # get id упомянутого юзера
                        mentioned_id = event.message['reply_message']['from_id']
                        # операции с рейтингом
                        social_credit[mentioned_id] += countSR

                        # вывод сообщения об изменении социального рейтинга
                        vk.messages.send(
                            chat_id = event.chat_id,
                            message = f'Пользователю {mentioned_id} добавлено {countSR} очков социального рейтинга.\nВсего: {social_credit[mentioned_id]}',
                            random_id = get_random_id()
                    )
                
    except Exception as e:
        vk.messages.send(
            chat_id = event.chat_id,
            message = f'{e}\n{traceback.format_exc()}',
            random_id = get_random_id()
        )

    continue
