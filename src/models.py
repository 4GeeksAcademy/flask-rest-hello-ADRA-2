from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    

    def __repr__(self):
        return '<User %r>' % self.first_name

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            # do not serialize the password, it's a security breach
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    gravity = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "gravity": self.gravity,
        "climate": self.climate,
        # do not serialize the password, it's a security breach
    }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_people = db.Column(db.String(252), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    mass = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name_people

    def serialize(self):
        return {
        "id": self.id,
        "name_people": self.name_people,
        "description": self.description,
        "mass": self.mass,
        "birth_year": self.birth_year,
        "gender": self.gender
        # do not serialize the password, it's a security breach
    }


class People_favorites(db.Model):
    __tablename__ = 'people_favorites'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user=db.relationship(User)
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))
    people = db.relationship(People)

    def __repr__(self):
        return '<People_favorites %r>' % self.name_people

    def serialize(self):
        return {"id": self.id,
                "user": self.user.first_name,
                "people": self.people.name_people}

class Planet_Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user=db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'))
    planet = db.relationship(Planet)

    def __repr__(self):
        return '<Planet_favorites %r>' % self.name

    def serialize(self):
        return {"id": self.id,
                "user": self.user.first_name,
                "planet": self.planet.name}