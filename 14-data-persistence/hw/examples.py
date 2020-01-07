import pymongo
import psycopg2
import redis
import storages


# sample data
class Sample():

    def __init__(self):
        self.foo = 456
        self.bar = 'kek'

    def get_quatro_foo(self):
        return self.foo**2


sample = Sample()

sample_dict = {'a': 1, 'b': 2, 'c': [1, 2, 5]}


print('init new instance of data storage module')
storage = storages.DataStorage()


print('filestorage save/load within one handler')
with open('file.txt', 'w+') as file:
    storage.save(sample, file, 'pickle')
    print(storage.load(file))

print('filestorage load after some time')
with open('file.txt', 'r') as file:
    sample_object_from_file = storage.load(file)
    print(sample_object_from_file)


print('mongodb within one connecttion')
with pymongo.MongoClient() as mongo_client:
    # you can save data with pickle serialize by default
    storage.save(sample, mongo_client)
    print(storage.load(mongo_client))


print('mongodb load data another connection')
with pymongo.MongoClient() as mongo_client:
    print(storage.load(mongo_client))


print('redis save/load within one connection')
with redis.Redis() as redis_client:
    # json exampe with dict data
    storage.save(sample_dict, redis_client, 'json')
    print(storage.load(redis_client))

print('redis load data another connection')
with redis.Redis() as redis_client:
    dict_from_redis = storage.load(redis_client)
    print(dict_from_redis)

# please, fill it to test PostgreSQL data storage
postgres_connection_credentials = {
    'dbname': '',
    'user': '',
    'password': '',
}

print('Postgres save/load data within one connection')
with psycopg2.connect(**postgres_connection_credentials) as postgres_client:
    storage.save(Sample, postgres_client)
    print(storage.load(postgres_client))

print('Postgres load data another connect')
with psycopg2.connect(**postgres_connection_credentials) as postgres_client:
    Sample_class_from_postgres = storage.load(postgres_client)
    print(Sample_class_from_postgres)


# it works!
print(Sample_class_from_postgres().get_quatro_foo())
print(sample_object_from_file.bar)
for pair in dict_from_redis.values():
    print(pair)
