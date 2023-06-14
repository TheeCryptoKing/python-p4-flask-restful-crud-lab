#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# /plants/:id
# fetch("http://localhost:5000/plants")

class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):

        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
# DELETE, PATCH

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)

    def patch(self, id):
        # newHeader = response.headers['Content-Type'] ='application/json'
        plants = Plant.query.filter(Plant.id == id).first()
        # The second one, filter_by(), may be used only for filtering by something specifically stated - a string or some number value. So it's usable only for category filtering, not for expression filtering.
        # On the other hand filter() allows using comparison expressions (==, <, >, etc.) so it's helpful e.g. when 'less/more than' filtering is needed. But can be used like filter_by() as well (when == used).
        # Just to remember both functions have different syntax for argument typing.
        
        # for patch in request.form:
        #     setattr(plants, patch, request.form[patch])
        # db.session.add(plants)
        # db.session.commit()
        # response_body = {
        #     "is_in_stock" : "false"
        # }
        # response = make_response(
        #     response_body,
        #     200
        #     )
        # return response
        
            # one or the other 
            
        #  code works
        # for patch in request.get_json():
        #     setattr(plants, patch, request.get_json(patch))
        # db.session.add(patch)
        # db.session.commit()
        # # printied in readme but i guess not asking for it 
        # response_body = {
        #     "is_in_stock" : "false"
        # }
        # response = make_response(
        #     response_body,
        #     200
        #     )
        # return response
        # looking for data = request.get_json() to pass tests
    def patch(self, id):

        data = request.get_json()

        plant = Plant.query.filter_by(id=id).first()

        for attr in data:
            setattr(plant, attr, data[attr])

        db.session.add(plant)
        db.session.commit()

        return make_response(plant.to_dict(), 200)

        # return make_response(plants.to_dict(), 200)


    def delete(self, id):
        plant = Plant.query.filter_by(id=id).first()
        plant = Plant.query.filter(Plant.id == id).first()
        db.session.delete(plant)
        db.session.commit()
        # not needed for no contetn in response body 
        # response_body = {
        #     "no content"
        # }
        # response = make_response(
        #     response_body,
        #     200
        # )
        # return response
        return make_response('', 204)
    

api.add_resource(PlantByID, '/plants/<int:id>')
        

if __name__ == '__main__':
    app.run(port=5555, debug=True)
