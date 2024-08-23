
from flask_login import UserMixin
from . import db
from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=True)
    bakiye = db.Column(db.Float, default=0.0)
    bakiye_ortak = db.Column(db.Boolean, default=False)
    def __str__(self):
        return f'{self.id}'
   
class Firma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    contact_person = db.Column(db.String(100), nullable=True)
    contact_number = db.Column(db.String(15), nullable=True)

    def __str__(self):
        return f'{self.id}'

class Otobus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('firma.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    plaka = db.Column(db.String(15), nullable=False)
    bakiye = db.Column(db.Float, default=0.0)
    tag_id = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    agent = db.relationship('Firma', backref=db.backref('otobusler',lazy='select'))
    user = db.relationship('User', backref=db.backref('otobusler', lazy='select'))

    def __str__(self):
        return f'{self.id}'

class Terminal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ekstra = db.Column(db.String(100), nullable=True)
    contact_person = db.Column(db.String(100), nullable=True)
    contact_number = db.Column(db.String(15), nullable=True)
    ucret = db.Column(db.Float, default=20.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __str__(self):
        return f'{self.id}'



class Gecis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gecis_zamani = db.Column(db.DateTime, default=datetime.utcnow)
    bus_id = db.Column(db.Integer, db.ForeignKey('otobus.id'), nullable=False)
    terminal_id = db.Column(db.Integer, db.ForeignKey('terminal.id'), nullable=False)
    odeme = db.Column(db.Float, default=20.0)

    otobus = db.relationship('Otobus', backref=db.backref('gecisler', lazy='select'))
    terminal = db.relationship('Terminal', backref=db.backref('gecisler', lazy='select'))

    def __str__(self):
        return f'{self.id}'

    