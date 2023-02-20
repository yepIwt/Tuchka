#!/usr/bin/python

"""
    Tuchka - open source cloud on VKontakte servers.
    yepIwt (Sergivesky Nikita), 2023
"""


import vk_api
from loguru import logger


def get_vk_api(
    login: str = None,
    password: str = None,
    token: str = None,
    ) -> tuple:

    logger.debug("Запуск функции get_vk_api")

    vk_session = vk_api.VkApi(
		login = login,
		password = password,
		token = token
	)

    api = vk_session.get_api()

    try:
        api.messages.getConversations()
    except Exception as err:
        logger.critical(f"Не получен VKAPI. {err}.")
        return False, err
    else:
        logger.debug("VKAPI успешно получен.")
        return True, api
