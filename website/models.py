from . import db
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func
from flask_login import UserMixin

class note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(200), nullable = False)
    video_id = db.Column(db.String(200), nullable = False)
    like = db.Column(db.Boolean)
    dislike = db.Column(db.Boolean)
    comments = db.Column(db.String)
    group = db.Column(db.Integer)
    def __repr__(self):
        return '<Name %r>' % self.id

class activity(db.Model):
    __bind_key__ = 'track.db'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(200), nullable=False)
    video_id = db.Column(db.String(200), nullable=False)
    percent_watched = db.Column(db.Float)
    paused = db.Column(db.Boolean)
    finished = db.Column(db.Boolean)
    group = db.Column(db.Integer)
    def __repr__(self):
        return '<Name %r>' % self.id

class user(db.Model, UserMixin):
    __bind_key__ = 'login.db'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    group = db.Column(db.Integer)
    def __repr__(self):
        return '<Name %r>' % self.id

class preference(db.Model):
    __bind_key__ = 'preferences.db'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String)
    ip = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    daily_vlog = db.Column(db.Integer)
    dressing = db.Column(db.Integer)
    fitness = db.Column(db.Integer)
    gourmet = db.Column(db.Integer)
    hair_braided = db.Column(db.Integer)
    homemade_drinks = db.Column(db.Integer)
    kids = db.Column(db.Integer)
    livehouse = db.Column(db.Integer)
    makeup = db.Column(db.Integer)
    painting = db.Column(db.Integer)
    pet = db.Column(db.Integer)
    photography = db.Column(db.Integer)
    popular_science = db.Column(db.Integer)
    scenery = db.Column(db.Integer)
    street_snap = db.Column(db.Integer)
    group = db.Column(db.Integer)
    def __repr__(self):
        return '<Name %r>' % self.id

class collection(db.Model):
    __bind_key__ = 'collection.db'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(200), nullable=False)
    video_id = db.Column(db.String(200), nullable=False)
    group = db.Column(db.Integer)
    def __repr__(self):
        return '<Name %r>' % self.id

class information(db.Model):
    __bind_key__ = 'personalInfo.db'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.String(200), nullable=False)
    group = db.Column(db.Integer)
    def __repr__(self):
        return '<Name %r>' % self.id

class browse(db.Model):
    __bind_key__ = 'browse.db'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(200), nullable=False)
    browsingTime = db.Column(db.Float, nullable=False)
    browsing_to_tot_ratio = db.Column(db.Float, nullable=False)
    path = db.Column(db.String)
    round_num = db.Column(db.Integer)
    code = db.Column(db.String)
    group = db.Column(db.Integer)
    def __repr__(self):
        return '<Name %r>' % self.id

class rating(db.Model):
    __bind_key__ = 'ratings.db'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(200), nullable=False)
    video_id = db.Column(db.String(200), nullable=False)
    relevance = db.Column(db.Integer)
    category = db.Column(db.String)
    responsive = db.Column(db.Integer)
    seconds = db.Column(db.Float)
    round_num = db.Column(db.Integer)
    group = db.Column(db.Integer)
    def __repr__(self):
        return '<Name %r>' % self.id

class btime(db.Model):
    __bind_key__ = 'browsingTime.db'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(200), nullable=False)
    ip = db.Column(db.String(200), nullable=False)
    page = db.Column(db.String)
    seconds = db.Column(db.Float)
    group = db.Column(db.Integer)
    def __repr__(self):
        return '<Name %r>' % self.id

class watch(db.Model):
    __bind_key__ = 'watch.db'
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String)
    video_id = db.Column(db.String(200), nullable=False)
    watch_time = db.Column(db.Float)
    vedio_time = db.Column(db.Float)
    percent = db.Column(db.Float)
    turn = db.Column(db.Integer)
    def __repr__(self):
        return '<Name %r>' % self.id

