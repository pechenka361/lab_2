from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields, reqparse
from random import random
from part.part import api as partns1
from part.parttmpl import api as partns2
from part.parttmpl import templ

app = Flask(__name__)
api = Api(app=app, 
        version='1.0',
        title='API Title',
        description='API Description',
        doc='/apidocs/')
name_space = api.namespace('main', description='Main APIs')

@name_space.route('/')
class Main(Resource):
    def get(self):
        return {'status': 'Got new data'}
    def post(self):
        return {'status': 'Posted new data'}

api.add_namespace(partns1)
api.add_namespace(partns2)
app.register_blueprint(templ, url_prefix='/templ')
list_ = api.model('list', {
    'len': fields.String(required=True, description='Size of array'),
    'array': fields.List(fields.String, required=True, description='Some array')
})

allarray = ['1']
name_space1 = api.namespace('list', description='list APIs')

@name_space1.route("/")
class ListClass(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(list_)
    def get(self):
        return {'len': str(len(allarray)), 'array':allarray}
    
    @name_space1.doc("")
    @name_space1.expect(list_)
    @name_space1.marshal_with(list_)
    def post(self):
        global allarray
        allarray = api.payload['array']
        return {'len': str(len(allarray)), 'array': allarray}

minmax = api.model('minmax', {'min':fields.String, 'max': fields.String}, required=True, description='two values')
@name_space1.route('/minmax')
class MinMaxClass(Resource):
    @name_space1.doc("")
    @name_space1.marshal_with(minmax)
    def get(self):
        global allarray
        return{'min': min(allarray), 'max': max(allarray)}
    
api.add_namespace(name_space1)

reqp = reqparse.RequestParser()
reqp.add_argument('len', type=int, required=False)
reqp.add_argument('minval', type=float, required=False)
reqp.add_argument('maxval', type=float, required=False)

@name_space1.route('/makerand')
class MakeArrayClass(Resource):
    @name_space1.doc("")
    @name_space1.expect(reqp)
    @name_space1.marshal_with(list_)
    def get(self):
        args = reqp.parse_args()
        array = [random()*(args['maxval'])+args['minval'] for i in range(args['len'])]
        return {"len": args["len"], "array": array}

app.run(debug=False)


