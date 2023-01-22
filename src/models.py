from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(120), unique=True, nullable=False)
    planet_climate = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.id 

    def serialize(self):
        return {
            "id": self.id,
            "planet_name": self.planet_name,
            "planet_climate": self.planet_climate,
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.Integer)
    hair = db.Column(db.String(250))
    eyes = db.Column(db.String(250))
    birth = db.Column(db.String(250))
    gender = db.Column(db.String(250))

    def __repr__(self):
        return '<People %r>' % self.name

    
    def serialize(self):
        return {
            "name": self.name,
            "height": self.height,
            "hair": self.hair,
            "eyes": self.eyes,
            "birth": self.birth,
            "gender": self.gender,
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    favorite_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    favorite_people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    favorite_planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    favorite_user = db.relationship('User')
    favorite_people = db.relationship('People')  
    favorite_planet = db.relationship('Planet')

    def __repr__(self):
        return '<Favorite %r>' % self.id

    
    def serialize(self):
        return {
            "favorite_user": self.favorite_user,
            "favorite_people": self.favorite_people,
            "favorite_planet": self.favorite_planet,
        }