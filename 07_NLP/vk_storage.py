import os
import json
import logging

logger = logging.getLogger(__name__)


class VKStorage:

    def __init__(self, folder):
        self.folder = folder
        self.__file_user_ids = '/{}/'.format(folder) + 'users_id.json'
        self.__file_users_age = '/{}/'.format(folder) + 'users_age.json'
        self.__file_users_info = '/{}/'.format(folder) + 'users_info.json'
        self.__file_users_wall = '/{}/'.format(folder) + 'users_posts.json'

    def save_users_id(self, users):
        logger.info('Saved user ids: file {}'.format(self.__file_user_ids))
        for user in users:
            self.__append_data(self.__file_user_ids, user)

    def save_users_age(self, users_age):
        logger.info('Saved users age: file {}'.format(self.__file_users_age))
        for user_age in users_age:
            self.__append_data(self.__file_users_age, user_age)

    def save_users_info(self, users_info):
        logger.info('Saved users info: file {}'.format(self.__file_users_info))
        for user_info in users_info:
            self.__append_data(self.__file_users_info, user_info)

    def save_users_wall(self, posts):
        logger.info('Saved users wall: file {}, posts count {}'.format(self.__file_users_wall, len(posts)))
        for post in posts:
            self.__append_data(self.__file_users_wall, post)

    def read_users_id(self):
        return self.__read_data(self.__file_user_ids)

    def read_users_age(self):
        return self.__read_data(self.__file_users_age)

    def read_users_info(self):
        return self.__read_data(self.__file_users_info)

    def read_users_posts(self):
        return self.__read_data(self.__file_users_wall)

    def __append_data(self, filename, data):
        filename = os.getcwd() + filename

        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        with open(filename, 'a') as fs:
            fs.write(json.dumps(data).replace('\n', ' ') + '\n')

    def __read_data(self, filename):
        if not os.path.exists(os.getcwd() + filename):
            logger.error('file not exists: ' + filename)
            raise StopIteration

        with open(os.getcwd() + filename, 'r') as fs:
            for line in fs:
                yield json.loads(line.strip())
