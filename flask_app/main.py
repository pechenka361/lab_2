from flask import Flask, Blueprint, request
from flask_restx import Api, Resource, fields, reqparse
from random import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Car, get_car_model, post_car_model, base_car_model
from parttmpl import templ

DATABASE_URL = "postgresql://postgres:OIyPyiqQtlXykdnpwGHeAYzpYUnrPtsr@postgres.railway.internal:5432/railway"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = Flask(__name__)
api = Api(app=app, 
        version='1.0',
        title='auto market',
        doc='/')

# app.register_blueprint(templ, url_prefix='/templ')

get_model = get_car_model(api)
post_model = post_car_model(api)
base_model = base_car_model(api)


Cars = api.namespace('cars', description='cars APIs')

@Cars.route("/get")
class GetClass(Resource):
    @Cars.doc(params={
            'order_by': {
                'description': 'Поле для сортировки (например, +year,-price)',
                'type': 'string',
                'default': '+year'
            }
        })
    @Cars.marshal_with(get_model)
    def get(self):
        with SessionLocal() as db:
            order_by = request.args.get('order_by', '').split(',')

            sort_fields = []
            allowed_fields = {'id', 'brand', 'model', 'year', 'price', 'mileage'}
            for field in order_by:
                field_name = field.lstrip('-+')
                if field_name in allowed_fields:
                    if field.startswith('-'):
                        sort_fields.append(getattr(Car, field_name).desc())
                    else:
                        sort_fields.append(getattr(Car, field_name).asc())

            cars_query = db.query(Car).order_by(*sort_fields).all()

            car_list = [
                {
                    "id": car.id,
                    "Brand": car.brand,
                    "Model": car.model,
                    "Year": car.year,
                    "Price": car.price,
                    "Mileage": car.mileage
                }
                for car in cars_query
            ]
            if car_list:
                years = [car["Year"] for car in car_list]
                price = [car["Price"] for car in car_list]
                mileage = [car["Mileage"] for car in car_list]
                result = {
                    "Cars": car_list,
                    "Total_cars": len(car_list),
                    "Year": {
                        "min": min(years), 
                        "max": max(years),
                        "avg": sum(years) / len(years)
                    },
                    "Price": {
                        "min": min(price), 
                        "max": max(price),
                        "avg": sum(price) / len(price)
                    },
                    "Mileage": {
                        "min": min(mileage), 
                        "max": max(mileage),
                        "avg": sum(mileage) / len(mileage)
                    }
                }
            else:
                result = {
                    "cars":[],
                    "total_cars": 0,
                    "Year": {
                        "min": None,
                        "max": None,
                        "avg": None,
                    },
                    "Price": {
                        "min": None,
                        "max": None,
                        "avg": None,
                    },
                    "Mileage": {
                        "min": None,
                        "max": None,
                        "avg": None,
                    }
                }
            return result
        
@Cars.route("/create")
class CreateClass(Resource):
    @Cars.doc('create car')
    @Cars.expect(post_model)
    @Cars.marshal_with(base_model, code=200)
    def post(self):
        with SessionLocal() as db:
            data = request.json
            new_car = Car(
                brand=data['Brand'],
                model=data['Model'],
                year=data['Year'],
                price=data['Price'],
                mileage=data['Mileage']
            )
            db.add(new_car)
            db.commit()
            car_list = {
                    "id": new_car.id,
                    "Brand": new_car.brand,
                    "Model": new_car.model,
                    "Year": new_car.year,
                    "Price": new_car.price,
                    "Mileage": new_car.mileage
                }
            return car_list, 200

@Cars.route("/update/<int:id>")
class UpdateClass(Resource):
    @Cars.doc('update car')
    @Cars.expect(post_model)
    @Cars.marshal_with(base_model, code=200)
    def put(self, id):
        with SessionLocal() as db:
            car = db.query(Car).filter(Car.id == id).first()
            if not car:
                api.abort(404, "Car not found")
            
            data = request.json
            car.brand = data.get('Brand', car.brand)
            car.model = data.get('Model', car.model)
            car.year = data.get('Year', car.year)
            car.price = data.get('Price', car.price)
            car.mileage = data.get('Mileage', car.mileage)
            db.commit()
            car_list = {
                "id": car.id,
                "Brand": car.brand,
                "Model": car.model,
                "Year": car.year,
                "Price": car.price,
                "Mileage": car.mileage
            }
            return car_list, 200
        
@Cars.route('/delete/<int:id>')
@Cars.param('id', 'Идентификатор автомобиля')
class CarsClass(Resource):
    @Cars.doc('delete_car')
    @Cars.response(200, 'Автомобиль успешно удален')
    @Cars.response(404, 'Автомобиль не найден')
    def delete(self, id):
        with SessionLocal() as db:
            car = db.query(Car).filter(Car.id == id).first()
            if not car:
                Cars.abort(404, "Автомобиль не найден")
            db.delete(car)
            db.commit()
            return 'Автомобиль успешно удален', 200
