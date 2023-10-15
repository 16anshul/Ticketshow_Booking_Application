from flask_login import UserMixin
from . import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    
    

class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    vname = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    venue_pic = db.Column(db.String)
    show = db.relationship('Show', backref='venue')


class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    sname = db.Column(db.String(100), nullable=False)
    sdate = db.Column(db.Date)
    stime = db.Column(db.Time)
    sduration = db.Column(db.Time)
    sdescription = db.Column(db.String(100), nullable=False)
    Tag = db.Column(db.String(100), nullable=False)
    Ticket_Price = db.Column(db.Integer, nullable=False)
    show_pic = db.Column(db.String)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venue.id', ondelete="CASCADE"), nullable=False)
    summary = db.relationship('Summary', backref='summary')
    

class Summary(db.Model):
    __tablename__ = 'summary'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    story = db.Column(db.Integer, nullable=False)
    visuals = db.Column(db.Integer, nullable=False)
    acting = db.Column(db.Integer, nullable=False)
    rewatchability = db.Column(db.Integer, nullable=False)
    overall_rating = db.Column(db.Integer, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True) 
    sname = db.Column(db.String(100), nullable=False)
    vaddress = db.Column(db.String(100), nullable=False)
    sdate = db.Column(db.Date)
    stime = db.Column(db.Time)
    price = db.Column(db.Integer, nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    sid = db.Column(db.Integer, nullable=False)
    uid = db.Column(db.Integer, nullable=False)
    