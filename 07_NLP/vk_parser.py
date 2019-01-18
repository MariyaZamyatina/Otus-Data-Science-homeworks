#from bs4 import BeautifulSoup
import pandas as pd
import logging
import os
import pickle
import pathlib
from vk_storage import VKStorage

logger = logging.getLogger(__name__)


class VKParser:

    def __init__(self, storage):
        self.__storage = storage
        self.df_folder = 'df_' + storage.folder
        self.__file_user_ids = '{}/'.format(self.df_folder) + 'users_id.pkl'
        self.__file_users_age = '{}/'.format(self.df_folder) + 'users_age.pkl'
        self.__file_users_info = '{}/'.format(self.df_folder) + 'users_info.pkl'
        self.__file_users_wall = '{}/'.format(self.df_folder) + 'users_posts.pkl'
        self.__file_raw_data = '{}/'.format(self.df_folder) + 'raw_data.pkl'

        if not os.path.exists(os.getcwd() + "/" + self.df_folder):
            os.makedirs(os.getcwd() + '/' + self.df_folder)

    def start(self):
        df_users_id = self.__parse_users_id()
        df_users_age = self.__parse_users_age()
        df_users_info = self.__parse_users_info()
        df_users_posts = self.__parse_users_posts()

        df = pd.merge(df_users_id, df_users_age, how='inner', on='id')
        df = pd.merge(df, df_users_info, how='inner', on='id')
        df = pd.merge(df, df_users_posts, how='left', on='id')

        with open(pathlib.Path(self.__file_raw_data).absolute(), 'wb') as f:
            pickle.dump(df, f)

        logger.info('Saved full data to the {} file'.format(self.__file_raw_data))

    def __parse_users_id(self):
        df = pd.DataFrame()

        for user_id in self.__storage.read_users_id():
            parsed_user_id = self.__parse_user_id(user_id)
            df = df.append(parsed_user_id, ignore_index=True)

        df['id'] = df['id'].astype(int)

        with open(self.__file_user_ids, 'wb') as f:
            pickle.dump(df, f)

        logger.info('users_id, shape {}'.format(df.shape))
        logger.info('Transformed data users_id saved to the {} file'.format(self.__file_user_ids))

        return df

    def __parse_users_age(self):
        df = pd.DataFrame()

        for user_age in self.__storage.read_users_age():
            df = df.append(user_age, ignore_index=True)

        df['id'] = df['id'].astype(int)
        df['age'] = df['age'].astype(int)

        with open(self.__file_users_age, 'wb') as f:
            pickle.dump(df, f)

        logger.info('users_age, shape {}'.format(df.shape))
        logger.info('Transformed data users_age saved to the {} file'.format(self.__file_users_age))

        return df

    def __parse_users_info(self):
        df = pd.DataFrame()

        for user_info in self.__storage.read_users_info():
            parsed_user_info = self.__parse_user_info(user_info)
            df = df.append(parsed_user_info, ignore_index=True)

        df['id'] = df['id'].astype(int)

        with open(self.__file_users_info, 'wb') as f:
            pickle.dump(df, f)

        logger.info('users_info, shape {}'.format(df.shape))
        logger.info('Transformed data users_info saved to the {} file'.format(self.__file_users_info))

        return df

    def __parse_users_posts(self):
        df = pd.DataFrame()

        prev_id = None
        text_list = []
        for user_posts in self.__storage.read_users_posts():
            id = user_posts['id']
            text = user_posts['text'] if 'text' in user_posts else ''

            # new user
            if prev_id and prev_id != id:
                df = df.append({'id': prev_id, 'posts': ' '.join(text_list)}, ignore_index=True)
                text_list = []

            text_list.append(text)
            prev_id = id

        #last user
        df = df.append({'id': prev_id, 'posts': ' '.join(text_list)}, ignore_index=True)

        df['id'] = df['id'].astype(int)

        with open(self.__file_users_wall, 'wb') as f:
            pickle.dump(df, f)

        logger.info('users_posts, shape {}'.format(df.shape))
        logger.info('Transformed data users_posts saved to the {} file'.format(self.__file_users_wall))

        return df


    def __parse_user_id(self, user_id):
        return {
                'id': user_id['id'],
                'first_name': user_id['first_name'],
                'last_name': user_id['last_name']
        }

    def __parse_user_info(self, user_info):
        return {
            'id': user_info['id'],
            'sex': user_info['sex'] if 'sex' in user_info else None,
            'bdate': user_info['bdate'] if 'bdate' in user_info else None,
            'country': user_info['country']['title'] if 'country' in user_info and 'title' in user_info['country'] else None,
            'city': user_info['city']['title'] if 'city' in user_info and 'title' in user_info['city'] else None,
            'has_photo': user_info['has_photo'] if 'has_photo' in user_info else None,
            'has_mobile': user_info['has_mobile'] if 'has_mobile' in user_info else None,
            'status': user_info['status'] if 'status' in user_info else None,
            'verified': user_info['verified'] if 'verified' in user_info else None,
            'followers_count': user_info['followers_count'] if 'followers_count' in user_info else None,
            'university': user_info['university'] if 'university' in user_info else None,
            'university_name': user_info['university_name'] if 'university_name' in user_info else None,
            'faculty': user_info['faculty'] if 'faculty' in user_info else None,
            'faculty_name': user_info['faculty_name'] if 'faculty_name' in user_info else None,
            'graduation': user_info['graduation'] if 'graduation' in user_info else None,
            'education_form': user_info['education_form'] if 'education_form' in user_info else None,
            'education_status': user_info['education_status'] if 'education_status' in user_info else None,
            'relation': user_info['relation'] if 'relation' in user_info else None,

            'interests': user_info['interests'] if 'interests' in user_info else '',
            'music': user_info['music'] if 'music' in user_info else '',
            'activities': user_info['activities'] if 'activities' in user_info else '',
            'movies': user_info['movies'] if 'movies' in user_info else '',
            'tv': user_info['tv'] if 'tv' in user_info else '',
            'books': user_info['books'] if 'books' in user_info else '',
            'games': user_info['games'] if 'games' in user_info else '',
            'schools': user_info['schools'] if 'schools' in user_info else None,
            'universities': user_info['universities'] if 'universities' in user_info else None,
            'about': user_info['about'] if 'about' in user_info else '',
            'quotes': user_info['quotes'] if 'quotes' in user_info else '',

            'personal_political': user_info['personal']['political'] if 'personal' in user_info and 'political' in user_info['personal'] else None,
            'personal_langs': user_info['personal']['langs'] if 'personal' in user_info and 'langs' in user_info['personal'] else None,
            'personal_religion': user_info['personal']['religion'] if 'personal' in user_info and 'religion' in user_info['personal'] else None,
            'personal_inspired_by': user_info['personal']['inspired_by'] if 'personal' in user_info and 'inspired_by' in user_info['personal'] else None,
            'personal_people_main': user_info['personal']['people_main'] if 'personal' in user_info and 'people_main' in user_info['personal'] else None,
            'personal_life_main': user_info['personal']['life_main'] if 'personal' in user_info and 'life_main' in user_info['personal'] else None,
            'personal_smoking': user_info['personal']['smoking'] if 'personal' in user_info and 'smoking' in user_info['personal'] else None,
            'personal_alcohol': user_info['personal']['alcohol'] if 'personal' in user_info and 'alcohol' in user_info['personal'] else None
        }
