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
    description = db.Column(db.String(100), nullable=False)
    gravity = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(100), nullable=False)

def __repr__(self):
        return '<Planet %r>' % self.description

def serialize(self):
    return {
        "id": self.id,
        "description": self.description,
        "gravity": self.gravity,
        "climate": self.climate,
        # do not serialize the password, it's a security breach
    }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    mass = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<People %r>' % self.description

def serialize(self):
    return {
        "id": self.id,
        "description": self.description,
        "mass": self.mass,
        "birth_year": self.birth_year,
        "gender": self.gender
        # do not serialize the password, it's a security breach
    }

class People_favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    User_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user=db.relationship(User)

def __repr__(self):
        return '<People %r>' % self.first_name

def serialize(self):
    return {"fisr_name": self.first_name}

class People_favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user=db.relationship(User)

def __repr__(self):
        return '<People %r>' % self.first_name

def serialize(self):
    return {"fisr_name": self.first_name}

class Planet_Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user=db.relationship(User)

    def __repr__(self):
        return '<Planet %r>' % self.irst_name

def serialize(self):
    return {"name": self.name}