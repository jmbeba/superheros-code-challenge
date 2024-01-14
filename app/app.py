#!/usr/bin/env python3

from flask import Flask, make_response, request
from flask_migrate import Migrate
from flask_restful import Resource, Api
from flask_cors import CORS

from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///heros.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class Home(Resource):
    def get(self):
        return make_response({
            "message":"Welcome to the superheroes api"
        })

api.add_resource(Home,'/')

class SuperHeros(Resource):
    def get(self):
        heroes = [hero.to_dict() for hero in Hero.query.all()]
        
        return make_response(
            heroes,
            200
        )

api.add_resource(SuperHeros,'/heroes')

class SuperHerosByID(Resource):
    def get(self,id):
        hero = Hero.query.filter(Hero.id == id).first()
        
        if not hero:
            return make_response(
                {
                    "error":"Hero not found",
                },
                404
            )
        
        return make_response(
            hero.to_dict(include_powers=True),
            200
        )
        
api.add_resource(SuperHerosByID,'/heroes/<int:id>')

class SuperPower(Resource):
    def get(self):
        powers = [power.to_dict() for power in Power.query.all()]
        
        return make_response(
            powers,
            200
        )
        
api.add_resource(SuperPower, '/powers')

class SuperPowerByID(Resource):
    def get(self, id):
        power = Power.query.filter(Power.id == id).first()
        
        if not power:
            return make_response(
                {"error":"Power not found"},
                404 
            )
            
        return make_response(
            power.to_dict(),
            200
        )
        
    def patch(self, id):
        power = Power.query.filter(Power.id == id).first()
        
        if not power:
            return make_response(
                {"error":"Power not found"},
                404 
            )
            
        try:
            for attr in request.json:
                setattr(power, attr, request.json.get(attr))
        except:
            return make_response(
                {
                    "errors": ["validation errors"]
                },
                400
            )
            
        db.session.add(power)
        db.session.commit()
            
        return make_response(
                power.to_dict(),
                200
            )
            
        
api.add_resource(SuperPowerByID, '/powers/<int:id>')

class SuperHeroPowers(Resource):
    def post(self):
        try:
            new_hero_power = HeroPower(
            strength=request.json.get('strength'),
            power_id=request.json.get('power_id'),
            hero_id=request.json.get('hero_id'),
            )
        except:
            return make_response(
                {
                    "errors": ["validation errors"]
                },
                400
            )
        
        db.session.add(new_hero_power)
        db.session.commit()
        
        hero = Hero.query.filter(Hero.id == new_hero_power.hero_id).first()
        
        return make_response(
            hero.to_dict(include_powers=True),
            200
        )
        
        
    
api.add_resource(SuperHeroPowers,'/hero_powers')

if __name__ == '__main__':
    app.run(port=5555)
