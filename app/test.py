from models import Hero
from app import app

with app.app_context():
    hero = Hero.query.first().to_dict(include_powers=True)
    print(hero)