import logging
import sys
import argparse

from storages.file_storage import JsonFileStorage
from scrappers.hh_scrapper import HeadHunterScrapper
from parsers.hh_parser import HeadHunterParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


#SCRAPPED_FILE = 'hh_scrapped_data.txt'
#TABLE_FORMAT_FILE = 'hh_data.csv'


def gather_process(search_text, num_pages, scrapped_file):
    logger.info("Gather process")

    storage = JsonFileStorage(scrapped_file)
    scrapper = HeadHunterScrapper(search_text, num_pages)
    scrapper.scrap_process(storage)


def convert_data_to_table_format(file_from, file_to):
    logger.info("transform")

    storage = JsonFileStorage(file_from)
    hh_parser = HeadHunterParser(file_to)
    hh_parser.parse(storage)


if __name__ == '__main__':
    logger.info("Work started")

    if sys.argv[1] == 'gather':
        parser = argparse.ArgumentParser()
        parser.add_argument('gather')
        parser.add_argument('--search')
        parser.add_argument('--pages')
        parser.add_argument('--file')
        args = parser.parse_args()

        gather_process(args.search, int(args.pages), args.file)

    elif sys.argv[1] == 'transform':
        parser = argparse.ArgumentParser()
        parser.add_argument('transform')
        parser.add_argument('--filefrom')
        parser.add_argument('--fileto')
        args = parser.parse_args()

        convert_data_to_table_format(args.filefrom, args.fileto)

    logger.info("Work ended")