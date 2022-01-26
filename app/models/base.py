from . import db
from datetime import datetime

class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_created = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    date_modified = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise(e)
    
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise(e)
        
