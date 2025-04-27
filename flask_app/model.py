from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import declarative_base
from flask_restx import fields
Base = declarative_base()

class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)  
    brand = Column(String, nullable=False)              
    model = Column(String, nullable=False)              
    year = Column(Integer, nullable=False)              
    price = Column(Float, nullable=False)               
    mileage = Column(Integer, nullable=False)           

def base_car_model(api):
    car_model = api.model('BaseCar', {
        'id': fields.Integer(required=True, description='Идентификатор'),
        'Brand': fields.String(required=True, description='Наименование бренда'),
        'Model': fields.String(required=True, description='Наименования модели'),
        'Year': fields.Integer(required=True, description='Год выпуска'),
        'Price': fields.Integer(required=True, description='Цена'),
        'Mileage': fields.Integer(required=True, description='Пробег')
    })
    return car_model

def get_car_model(api):
    car_model = base_car_model(api)
    cars_list_model = api.model('CarsList', {
    'Cars': fields.List(fields.Nested(car_model), description='Список автомобилей'),
    'Total_cars': fields.Integer(required=True, description='Количество автомобилей'),
    'Year': fields.Raw(required=True, description='Количество автомобилей'),
    'Price': fields.Raw(required=True, description='Количество автомобилей'),
    'Mileage': fields.Raw(required=True, description='Количество автомобилей'),
    })
    return cars_list_model

def post_car_model(api):
    car_model = api.model('PostCar', {
        'Brand': fields.String(required=True, description='Наименование бренда'),
        'Model': fields.String(required=True, description='Наименования модели'),
        'Year': fields.Integer(required=True, description='Год выпуска'),
        'Price': fields.Integer(required=True, description='Цена'),
        'Mileage': fields.Integer(required=True, description='Пробег')
    })
    return(car_model)