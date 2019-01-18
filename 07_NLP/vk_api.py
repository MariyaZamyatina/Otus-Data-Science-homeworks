import logging
import requests
import time

logger = logging.getLogger(__name__)

CURRENT_YEAR = 2018


class VKApiConnector(object):
    __base_url = 'https://api.vk.com/method/'
    __users_search_method = 'users.search'
    __users_get_method = "users.get"
    __wall_get_method = 'wall.get'
    __v = NotImplemented
    __token = NotImplemented
    __client_id = NotImplemented
    __sleep_time = NotImplemented
    __storage = NotImplemented

    __user_info_fields = 'verified, sex, bdate, city, country, has_photo, \
                            has_mobile, education, universities, schools, \
                            status, followers_count, relation, personal, \
                            activities, interests, music, movies, tv, books, \
                            games, about, quotes, maiden_name'

    @classmethod
    def config(cls, version, client_id, token, sleep_time=0.5):
        cls.__v = version
        cls.__sleep_time = sleep_time
        cls.__client_id = client_id
        cls.__token = token

    @classmethod
    def storage(cls, storage):
        cls.__storage = storage

    @classmethod
    def __get_base_request_params(cls):
        return {
            'v': cls.__v,
            'access_token': cls.__token,
            'client_id': cls.__client_id
        }

    @classmethod
    def get_random_users_id(cls, sex=0, birth_year=None, count=1000, offset=None):
        """
        Получить рандомные профили в одном запросе - max 1000 пользователей.
        Информация сохраняется в файл.
        """
        response = cls.__request_user_search(sex, birth_year, count, offset)
        time.sleep(cls.__sleep_time)

        if response and 'items' in response:
            users = response['items']
            users = cls.__filter_closed_profiles(users)
            users_age = [{'id': user['id'], 'age': CURRENT_YEAR - birth_year} for user in users]

            cls.__storage.save_users_id(users)
            cls.__storage.save_users_age(users_age)
            return users

    @classmethod
    def __filter_closed_profiles(cls, users):
        """
        Отфильтровать закрытые профили
        """
        filter_users = [user for user in users if not user['is_closed'] or user['can_access_closed']]
        logger.info('Filtered user ids: count before {}, count after {}'.format(len(users), len(filter_users)))
        return filter_users

    @classmethod
    def get_users_info(cls, users_id, fields=None):
        """
        Получить информацию со страницы пользователей.
        :param users_id: массив id пользователей
        :param fields: поля со страницы пользователей для загрузки
        """
        response = cls.__request_users_get(users_id, fields)
        time.sleep(cls.__sleep_time)

        if response:
            cls.__storage.save_users_info(response)

    @classmethod
    def get_users_wall(cls, users_id, count=100):
        for user_id in users_id:
            response = cls.__request_wall_get(user_id, count=count)
            time.sleep(cls.__sleep_time)

            if response and ('items' in response) and (len(response['items']) != 0):
                posts = []
                for item in response['items']:
                    if item['text'] != '':
                        post = {'id': user_id,
                                'text': item['text']
                                }
                        posts.append(post)
                cls.__storage.save_users_wall(posts)

    @classmethod
    def __request_user_search(cls, sex=0, birth_year=None, count=1000, offset=None):
        try:
            logger.info('Access {} method: sex={}, birth_year={}, count={}, offset={}'.\
                            format(cls.__users_search_method, sex, birth_year, count, offset))
            request_params = cls.__get_base_request_params()
            request_params['count'] = count
            request_params['sex'] = sex

            if offset is not None:
                request_params['offset'] = offset
            if birth_year is not None:
                request_params['birth_year'] = birth_year

            url = '{}{}'.format(cls.__base_url, cls.__users_search_method)
            response = requests.post(url, request_params if request_params else None)

            if not response.ok or 'response' not in response.json():
                logger.error(response.text)
                return None
            else:
                return response.json()['response']

        except Exception as ex:
            logger.exception(ex)

    @classmethod
    def __request_users_get(cls, users_ids, fields=None):
        try:
            logger.info('Access {} method'.format(cls.__users_get_method))
            request_params = cls.__get_base_request_params()
            request_params['user_ids'] = str(users_ids).strip('[]').replace(" ", "")
            request_params['fields'] = fields if fields else cls.__user_info_fields

            url = '{}{}'.format(cls.__base_url, cls.__users_get_method)
            response = requests.post(url, request_params if request_params else None)

            if not response.ok or 'response' not in response.json():
                logger.error(response.text)
                return None
            else:
                return response.json()['response']
        except Exception as ex:
            logger.exception(ex)

    @classmethod
    def __request_wall_get(cls, user_id, count=100):
        try:
            logger.info("Access {} method: user_id {}, count {}".format(cls.__wall_get_method, user_id, count))
            request_params = cls.__get_base_request_params()
            request_params['owner_id'] = user_id
            request_params['count'] = count

            url = '{}{}'.format(cls.__base_url, cls.__wall_get_method)
            response = requests.post(url, request_params if request_params else None)

            if not response.ok or 'response' not in response.json():
                logger.error(response.text)
            else:
                return response.json()['response']
        except Exception as ex:
            logger.exception(ex)



