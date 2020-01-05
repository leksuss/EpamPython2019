import json
import pickle


class DataStorage():

    get_storages = {}

    def __init__(self):
        self.__class__.collect_storages()
        self.data = ''
        self.ser_type = 'json'  # value by default
        self.handler = 'redis'  # value by default

    @classmethod
    def collect_storages(cls):
        for storage_class in cls.__subclasses__():
            cls.get_storages[storage_class.handler_class] = storage_class

    def json_serialize(self):
        return json.dumps(self.data)

    def json_deserialize(self):
        return json.loads(self.data)

    def serialize(self):
        if self.ser_type == 'json':
            return self.json_serialize()
        elif self.ser_type == 'pickle':
            pass

    def deserialize(self):
        if self.ser_type == 'json':
            return self.json_deserialize()
        elif self.ser_type == 'pickle':
            pass

    def save(self, data, handler='', ser_type=''):
        self.data = data
        if handler:
            self.handler = handler
        if ser_type:
            self.ser_type = ser_type
        serialized_data = self.serialize()
        # print(self.handler.__name__)

    def load():
        pass


class Redis(DataStorage):

    handler_module_name = 'redis'

    def save(self, data, handler, ser_type=''):
        pass

    def load(self, handler):
        pass


class Postgres(DataStorage):

    handler_module_name = 'psycopg2'

    def save(self, data, handler, ser_type):
        pass

    def load(self, handler):
        pass


