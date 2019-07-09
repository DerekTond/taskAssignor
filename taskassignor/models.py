from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Task(db.Model):
    # model
    r_id = db.Column(db.Integer, primary_key=True)
    batch_id = db.Column(db.String(160))
    id = db.Column(db.Integer)
    info = db.Column(db.String(400), nullable=False)
    checked_info = db.Column(db.String(400))
    status = db.Column(db.String(40))
    checker = db.Column(db.String(40))
    time = db.Column(db.DateTime)