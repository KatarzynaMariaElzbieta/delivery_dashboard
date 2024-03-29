from geoalchemy2 import Geometry
from sqlalchemy import (ARRAY, DECIMAL, Column, DateTime, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import declarative_base, relationship

# from dashboard_app.models.orm_settings import engine

Base = declarative_base()


class Restaurants(Base):
    __tablename__ = "restaurants"
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    location = Column(Geometry(geometry_type="POINT", srid=4326))
    type_id = Column(Integer)
    address = Column(String, unique=True)
    orders = relationship("Orders", back_populates="restaurant")


class Deliverers(Base):
    __tablename__ = "deliverers"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)
    orders = relationship("Orders", back_populates="deliverer")


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
    delivery_problems = Column(ARRAY(Integer))
    food_problems = Column(ARRAY(Integer))
    description = Column(String)
    rating = Column(Integer)


# Base.metadata.create_all(engine)
