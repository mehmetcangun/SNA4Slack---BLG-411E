import datetime

import src.models.DB as DB
import src.models.User
import src.models.SNAPreferences

db = DB.db
class FileInfo(db.Model):
    __tablename__ = "fileinfo"

    id = db.Column(db.Integer, primary_key=True)
    file_size = db.Column(db.String(20), nullable=False)
    is_proper = db.Column(db.Boolean, nullable=False, default=True)
    uploaded_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    preferences = db.relationship('SNAPreferences', backref='fileinfo', lazy=True)


class FileInfoQuery():
    fileinfo = None
    def __init__(self, user_id, file_size, is_proper) -> None:
        self.fileinfo = FileInfo(user_id=user_id, file_size=file_size, is_proper=is_proper)
    
    def save_fileinfo(self):
        db.session.add(self.fileinfo)
        db.session.commit()
    
    