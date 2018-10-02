import os
import json
import logging

logger = logging.getLogger(__name__)


class JsonFileStorage:

    def __init__(self, file_name):
        self.file_name = file_name

    def read_json_object(self):
        if not os.path.exists(self.file_name):
            logger.error('file not exists: ' + self.file_name)
            raise StopIteration

        with open(self.file_name, 'r') as fs:
            for line in fs:
                yield json.loads(line.strip())

    def append_json_object(self, json_object):
        with open(self.file_name, 'a') as fs:
            fs.write(json.dumps(json_object).replace('\n', ' ') + '\n')