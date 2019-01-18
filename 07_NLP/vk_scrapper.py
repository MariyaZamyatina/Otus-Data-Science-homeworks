import logging
import configparser

from vk_api import VKApiConnector
from vk_storage import VKStorage

logger = logging.getLogger(__name__)


class VKScrapper:

    def __init__(self, filename_config, folder_data):
        self.__filename_config = filename_config
        self.__folder_data = folder_data

    def read_config(self):
        config = configparser.ConfigParser()
        config.read(self.__filename_config)

        vk_api_v = config.get('VKApi', "v")
        vk_api_token = config.get('VKApi', 'token')
        client_id = config.get('VKApi', 'client_id')
        VKApiConnector.config(vk_api_v, client_id, vk_api_token)

    def prepare_storage(self):
        VKApiConnector.storage(VKStorage(self.__folder_data))

    def scrap_users_process(self, birth_years, count=500, offset=0):
        for year in birth_years:
            for sex in [1, 2]:
                users = VKApiConnector.get_random_users_id(sex=sex, birth_year=year, count=count, offset=offset)
                users_id = [user['id'] for user in users]

                VKApiConnector.get_users_info(users_id)
                VKApiConnector.get_users_wall(users_id, 100)
