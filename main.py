import os
from unicodedata import name
from dotenv import load_dotenv
import ast
import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from models import Book, Publisher, Sale, Shop, Stock, Base
# from sqlalchemy_fixture import FixtureRegistry, fixture, last_fixture

def load_data(engine):
    file = open("fixtures/tests_data.json", "r")
    contents = file. read()
    dictionary = ast.literal_eval(contents)
    file.close()
         
    # for item in dictionary:
    #     obj = fixture(item.model, item.fields)

    # Через sqlalchemy_fixture не получилось, делаем через ORM

    Session = sessionmaker(bind=engine)
    session = Session()

    for item in dictionary:
        
        if item['model'] == "publisher":
            # {"model": "publisher", "pk": 2, "fields": {"name": "Pearson"}}
            obj = Publisher(id=item['pk'], name=item['fields']['name'])

        elif item['model'] == "book":
            # {"model": "book", "pk": 1, "fields": {"title": "Programming Python, 4th Edition", "publisher": 1}}
            obj = Book(id=item['pk'], title=item['fields']['title'], id_publisher=item['fields']['publisher'])

        elif item['model'] == "shop":
            # {"model": "shop", "pk": 1, "fields": {"name": "Labirint"}}
            obj = Shop(id=item['pk'], name=item['fields']['name'])

        elif item['model'] == "stock":
            # {"model": "stock", "pk": 1, "fields": {"shop": 1, "book": 1, "count": 34}}
            obj = Stock(id=item['pk'], id_shop=item['fields']['shop'], id_book=item['fields']['book'], count=item['fields']['count'])

        elif item['model'] == "sale":
            # {"model": "sale", "pk": 1, "fields": {"price": "50.05", "date_sale": "2018-10-25T09:45:24.552Z", "count": 16, "stock": 1}}
            obj = Sale(id=item['pk'], price=item['fields']['price'], date_sale=item['fields']['date_sale'], count=item['fields']['count'], id_stock=item['fields']['stock'])

        session.add(obj)

    session.commit() 

    
def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def create_engine():
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    DSN = os.getenv("DSN")
    return sq.create_engine(DSN)


if __name__ == '__main__':

    engine = create_engine()

    create_tables(engine)
    load_data(engine)

    publisher_id = int(input("Введите ID издателя: "))

    Session = sessionmaker(bind=engine)
    session = Session()

    q = session.query(Publisher).filter(Publisher.id == publisher_id)
    if len(q.all()) != 0:
        for s in q.all():
            print(s.name)
    else:
        print("Издатель не найден")
    
