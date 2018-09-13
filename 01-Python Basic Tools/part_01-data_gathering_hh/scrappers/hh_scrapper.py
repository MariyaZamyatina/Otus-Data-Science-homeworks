import requests
import json
import logging

logger = logging.getLogger(__name__)

# строка поиска вакансий
SEARCH_TEXT = '!"data science" OR !"data scientist" OR !"machine learning" OR !"Deep Learning" ' \
              'OR !"Data Analysis" OR ' \
              '!"Big data" OR Hadoop OR Spark '
# число ваканский на странице, max = 100 - ограничение API
NUM_PER_PAGE = 100
# число страниц
NUM_PAGES = 10


class HeadHunterScrapper(object):

    def __init__(self):
        pass

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
        logger.info('text: {}'.format(SEARCH_TEXT))
        logger.info('per_page: {}'.format(NUM_PER_PAGE))
        logger.info('pages: {}'.format(NUM_PAGES))

        vacancy_urls = []
        for i in range(0, NUM_PAGES):
            url = 'https://api.hh.ru/vacancies?text={0}&per_page={1}&page={2}'.format(SEARCH_TEXT, NUM_PER_PAGE, str(i))
            vacancy_urls += self.get_vacancy_urls(url)

        vacancy_num = 0
        for vacancy_url in vacancy_urls:
            response = requests.get(vacancy_url)
            if response.ok:
                vacancy_data = response.json()
                storage.append_json_object(vacancy_data)
                vacancy_num += 1

        logger.info('Save {} vacancies from hh.ru to the {} file'.format(vacancy_num, storage.file_name))
