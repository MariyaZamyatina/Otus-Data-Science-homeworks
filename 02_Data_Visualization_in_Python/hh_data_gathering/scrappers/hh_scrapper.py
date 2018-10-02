import requests
import json
import logging
import math
from tqdm import tqdm

logger = logging.getLogger(__name__)

NUM_PER_PAGE = 100
MAX_PER_SEARCH = 2000

class HeadHunterScrapper(object):

    def __init__(self, search_text, num_pages):
        self._search_text = search_text
        self._num_pages = num_pages

    def get_vacancy_urls(self, url):
        response = requests.get(url)

        if not response.ok:
            logger.error('response error, url: ' + url)
            return []
        else:
            vacancy_urls = [item['url'] for item in response.json()['items']]

        return vacancy_urls

    def scrap_process(self, storage):
        logger.info('Getting data from hh.ru...')
        logger.info('search_text: {}'.format(self._search_text))
        logger.info('per_page: {}'.format(NUM_PER_PAGE))
        logger.info('pages: {}'.format(self._num_pages))

        vacancy_urls = []

        for i in range(self._num_pages):
            url = 'https://api.hh.ru/vacancies?text={0}&per_page={1}&page={2}'.format(self._search_text, NUM_PER_PAGE, str(i))
            vacancy_urls += self.get_vacancy_urls(url)

        vacancy_num = 0
        for vacancy_url in tqdm(vacancy_urls):
            response = requests.get(vacancy_url)
            if response.ok:
                vacancy_data = response.json()
                storage.append_json_object(vacancy_data)
                vacancy_num += 1

        logger.info('Save {} vacancies from hh.ru to the {} file'.format(vacancy_num, storage.file_name))
