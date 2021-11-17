from pymongo import MongoClient
from pprint import pprint

client = MongoClient("127.0.0.1",27017)

db = client['users1611']
books = db.books
persons = db.persons

persons.collection.create_index('author', name='search_index')
doc = {
    'author': "Peter",
    "age" : 38,
    "text" : "is cool",
    "tag":['cool','hot','ice'],
    "date":"14.06.1983"
}

for doc in persons.find({}):
    pprint(doc)


#print(f"Документ {doc['_id']} существует")

print(persons.find())


