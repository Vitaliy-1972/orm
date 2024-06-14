import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Stock, Sale, Shop

dialect = 'postgresql'
user = 'postgres'
password = 'af49vo'
host = 'localhost'
port = 5432
database = 'python_db'

dsn = f'{dialect}://{user}:{password}@{host}:{port}/{database}'
engine = sqlalchemy.create_engine(dsn)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()
with open('tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


def gets_shops(a):
    res = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).select_from(Shop). \
        join(Stock). \
        join(Book). \
        join(Publisher). \
        join(Sale)
    if a.isdigit():
        b = res.filter(int(a) == Publisher.id).all()
    else:
        b = res.filter(a == Publisher.name).all()
    for bk, sh, sa, sd in b:
        print(f"{bk:<40} | {sh:<10} | {sa:<8} | {sd.strftime('%d-%m-%Y')} ")


if __name__ == '__main__':
    a = input('Введите имя или айди публициста ')
    gets_shops(a)

session.close()
