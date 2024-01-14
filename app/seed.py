from models import db, Power, Hero, HeroPower
from random import randint, choice
from app import app

with app.app_context():
    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()
    print("🦸‍♀️ Seeding powers...")
    powers = [
        {"name": "Super Strength", "description": "Gives the wielder super-human strengths"},
        {"name": "Flight", "description": "Gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "Superhuman Senses", "description": "Allows the wielder to use her senses at a super-human level"},
        {"name": "Elasticity", "description": "Can stretch the human body to extreme lengths"},
    ]
    for power_data in powers:
        power = Power(**power_data)
        db.session.add(power)
    db.session.commit()

    print("🦸‍♀️ Seeding heroes...")
    heroes = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"},
    ]
    for hero_data in heroes:
        hero = Hero(**hero_data)
        db.session.add(hero)
    db.session.commit()

    print("🦸‍♀️ Adding powers to heroes...")
    strengths = ["Strong", "Weak", "Average"]
    for hero in Hero.query.all():
        for _ in range(randint(1, 3)):
            power = choice(Power.query.all())
            heropower = HeroPower(hero_id=hero.id, power_id=power.id, strength=choice(strengths))
            db.session.add(heropower)
        db.session.commit()

    print("🦸‍♀️ Done seeding!")

