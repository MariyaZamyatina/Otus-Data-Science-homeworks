from bs4 import BeautifulSoup
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class HeadHunterParser:
    def __init__(self, table_format_file):
        self.table_format_file = table_format_file

    def parse_vacancy(self, vacancy):
        return {'id': vacancy['id'],
                'description': BeautifulSoup(vacancy['description'], 'lxml').text,
                'has_branded_description': vacancy['branded_description'] is not None,
                'key_skills': ', '.join([skill['name'] for skill in vacancy['key_skills']]),
                'schedule': vacancy['schedule']['id'],
                'accept_handicapped': vacancy['accept_handicapped'],
                'experience': vacancy['experience']['id'],
                'address_lat': vacancy['address']['lat'] if vacancy['address'] is not None else None,
                'address_lng': vacancy['address']['lng'] if vacancy['address'] is not None else None,
                'metro_stations': vacancy['address']['metro_stations'] if vacancy['address'] is not None else None,
                'address_city': vacancy['address']['city'] if vacancy['address'] is not None else None,
                'employment': vacancy['employment']['id'] if vacancy['employment'] is not None else None,
                'salary_from': vacancy['salary']['from'] if vacancy['salary'] is not None else None,
                'salary_to': vacancy['salary']['to'] if vacancy['salary'] is not None else None,
                'salary_gross': vacancy['salary']['gross'] if vacancy['salary'] is not None else None,
                'salary_currency': vacancy['salary']['currency'] if vacancy['salary'] is not None else None,
                'name': vacancy['name'],
                'published_at': vacancy['published_at'],
                'employer_name': vacancy['employer']['name'],
                'type': vacancy['type']['id'],
                'has_test': vacancy['has_test'],
                #'specializations': vacancy['specialization'],
                'premium': vacancy['premium']
                }

    def parse(self, storage):
        df = pd.DataFrame()

        for json_object in storage.read_json_object():
            parsed_vacancy = self.parse_vacancy(json_object)
            df = df.append(parsed_vacancy, ignore_index=True)

        df.to_csv(self.table_format_file, sep='\t', index=False)

        logger.info('Transformed data saved to the {} file'.format(self.table_format_file))