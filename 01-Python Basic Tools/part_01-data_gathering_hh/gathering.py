import logging
import sys

from storages.file_storage import JsonFileStorage
from scrappers.hh_scrapper import HeadHunterScrapper
from parsers.hh_parser import HeadHunterParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


SCRAPPED_FILE = 'hh_scrapped_data.txt'
TABLE_FORMAT_FILE = 'hh_data.csv'


def gather_process():
    logger.info("Gather process")

    storage = JsonFileStorage(SCRAPPED_FILE)
    scrapper = HeadHunterScrapper()
    scrapper.scrap_process(storage)


def convert_data_to_table_format():
    logger.info("transform")

    storage = JsonFileStorage(SCRAPPED_FILE)
    hh_parser = HeadHunterParser(TABLE_FORMAT_FILE)
    hh_parser.parse(storage)


if __name__ == '__main__':
    logger.info("Work started")

    if sys.argv[1] == 'gather':
        gather_process()

    elif sys.argv[1] == 'transform':
        convert_data_to_table_format()

    logger.info("Work ended")