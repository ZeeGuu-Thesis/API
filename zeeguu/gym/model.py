# -*- coding: utf8 -*-
import datetime

from zeeguu import db


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer)
    contribution_id = db.Column(db.Integer, db.ForeignKey('contribution.id'))
    contribution = db.relationship("Contribution", backref="card")
    last_seen = db.Column(db.DateTime)

    def __init__(self, contribution):
        self.contribution = contribution
        self.position = 0
        self.seen()

    def seen(self):
        self.last_seen = datetime.datetime.now()
