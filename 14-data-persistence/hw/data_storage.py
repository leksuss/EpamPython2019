import pickle
import psycopg2
import redis
import storages


r = redis.Redis(host='localhost', port=6379, db=0)
print(type(r).__module__.split('.')[0])


dict = {'a': 1, 'b': 2, 'c': [1, 2, 3]}

place = storages.DataStorage()

res = place.save(dict, r, 'json')
print(place.__dict__)
print(res)



conn = psycopg2.connect(dbname='goldena_ru', user='goldena_ru_user',
                        password='goldena_ru!', host='localhost')
cursor = conn.cursor()
print(conn)
print(type(conn).__module__.split('.')[0])
print("{0}.{1}".format(conn.__class__.__module__,conn.__class__.__name__))
'''
cursor.execute('CREATE TABLE IF NOT EXISTS data_storage (
                    id serial PRIMARY KEY,
                    json_data json,
                    binary_data text);
                ')
cursor.execute("""SELECT table_name FROM information_schema.tables
       WHERE table_schema = 'public'""")
for table in cursor.fetchall():
    print(table)

conn.commit()
conn.close()
'''


