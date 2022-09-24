from geoalchemy2 import Geometry
from sqlalchemy import (DECIMAL, Column, DateTime, ForeignKey, Identity,
                        Integer, String)
from sqlalchemy.orm import declarative_base, relationship

# from orm_settings import engine

Base = declarative_base()


class Restaurants(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    location = Column(Geometry)
    type_id = Column(Integer)
    address = Column(String(200))
    children = relationship("Orders", back_populates="restaurants")


class Deliverers(Base):
    __tablename__ = "deliverers"
    id = Column(Integer, primary_key=True)
    name = Column(String(120))


class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    restaurant = relationship(Restaurants, back_populates="orders")
    costs_of_food = Column(DECIMAL)
    means_of_transport = Column(Integer)
    cost_of_delivery = Column(DECIMAL)
    order_create_date = Column(DateTime)
    delivery_datetime = Column(DateTime)
    deliverer_id = Column(Integer, ForeignKey("deliverers.id"))
    deliverer = relationship(Deliverers, back_populates="orders")
    delivery_problems = Column(String)
    food_problems = Column(Integer)
    description = Column(String)
    rating = Column(Integer)


# Base.metadata.create_all(engine)
