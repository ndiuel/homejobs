from . import db
from .base import BaseModel


class Chat(db.Model, BaseModel):
    user_1_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_2_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    updated = db.Column(db.Integer, default=0)
    


class ChatViews(db.Model, BaseModel):
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    

class ChatMessages(db.Model, BaseModel):
    message = db.Column(db.Text)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))
    receiver_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    