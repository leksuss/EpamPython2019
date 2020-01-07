import json
import pickle
import base64
from abc import ABC, abstractmethod


class DataStorage():

    get_storages = {}

    def __init__(self):
        self.data = ''
        self.ser_type = ''
        self.handler = ''
        self.__class__.collect_storages(AbstractStorage)

    @classmethod
    def collect_storages(cls, AbstractStorage):
        for storage_class in AbstractStorage.__subclasses__():
            cls.get_storages[storage_class.module_name] = storage_class

    def get_storage_module_name(self):
        return type(self.handler).__module__.split('.')[0]

    def json_serialize(self):
        return json.dumps(self.data)

    def json_deserialize(self):
        return json.loads(self.data)

    def pickle_serialize(self):
        to_bytes = pickle.dumps(self.data)
        return base64.b64encode(to_bytes).decode()

    def pickle_deserialize(self):
        to_bytes = base64.b64decode(self.data.encode())
        return pickle.loads(to_bytes)

    def serialize(self):
        if self.ser_type == 'json':
            return self.json_serialize()
        elif self.ser_type == 'pickle':
            return self.pickle_serialize()
        else:
            raise AttributeError(
                f'{self.ser_type} serializing is not available')

    def deserialize(self):
        if self.ser_type == 'json':
            return self.json_deserialize()
        elif self.ser_type == 'pickle':
            return self.pickle_deserialize()
        else:
            raise AttributeError(
                f'{self.ser_type} deserializing is not available')

    def save(self, data, handler, ser_type=''):
        self.data = data
        self.handler = handler
        self.ser_type = ser_type or 'pickle'  # value by default
        serialized_data = self.serialize()
        module_name = self.get_storage_module_name()
        res = self.get_storages[module_name](
            self.handler,
            self.ser_type,
            serialized_data).save()
        return res

    def load(self, handler):
        self.handler = handler
        module_name = self.get_storage_module_name()
        self.ser_type, self.data = \
            self.get_storages[module_name](self.handler).load()
        return self.deserialize()


class AbstractStorage(ABC):

    def __init__(self, handler, ser_type='', data=''):
        self.handler = handler
        self.ser_type = ser_type
        self.data = data

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def load(self):
        pass


class MongoStorage(AbstractStorage):

    module_name = 'pymongo'

    def __init__(self, handler, ser_type='', data=''):
        super().__init__(handler, ser_type, data)
        self.database = self.handler['data_storage']
        self.collection = self.database.collection

    def save(self):
        self.collection.drop()
        data = {'ser_type': self.ser_type, 'data': self.data}
        self.collection.insert_one(data)

    def load(self):
        result = self.collection.find({})
        return (result[0]['ser_type'], result[0]['data'])


class FileStorage(AbstractStorage):

    module_name = '_io'

    def save(self):
        self.handler.seek(0)
        self.handler.truncate()
        self.handler.write(self.ser_type + '\n' + self.data)
        self.handler.flush()

    def load(self):
        self.handler.seek(0)
        data = self.handler.readlines()
        return (line.strip() for line in data)


class RedisStorage(AbstractStorage):

    module_name = 'redis'

    def save(self):
        return all(
            (self.handler.set('ser_type', self.ser_type),
             self.handler.set('data', self.data))
        )

    def load(self):
        return self.handler.get('ser_type').decode(), \
            self.handler.get('data').decode()


class PostgresStorage(AbstractStorage):

    module_name = 'psycopg2'

    def __init__(self, handler, ser_type='', data=''):
        super().__init__(handler, ser_type, data)
        self.cursor = self.handler.cursor()
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS data_storage (
                id serial PRIMARY KEY,
                ser_type VARCHAR (100),
                data text);
            """)

    def save(self):
        with self.cursor as cursor:
            self.cursor.execute("TRUNCATE data_storage RESTART IDENTITY")
            self.cursor.execute(
                f"""
                INSERT INTO data_storage (ser_type, data)
                VALUES ('{self.ser_type}', '{self.data}')
                """)

    def load(self):
        with self.cursor as cursor:
            cursor.execute(
                "SELECT ser_type, data FROM data_storage where id=1"
            )
            return cursor.fetchall()[0]
