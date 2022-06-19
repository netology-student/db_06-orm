import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50))


class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=50))
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="books")


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=50))


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    book = relationship(Book, backref="stocks")

    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    shop = relationship(Shop, backref="stocks")
    
    count = sq.Column(sq.Integer)


class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float);
    date_sale = sq.Column(sq.DateTime)
    
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    stock = relationship(Stock, backref="sales")

    count = sq.Column(sq.Integer)