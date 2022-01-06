import datetime

import src.models.DB as DB
import src.models.User
import src.models.SNAPreferences

db = DB.db
class FileInfo(db.Model):
    __tablename__ = "fileinfo"

    id = db.Column(db.Integer, primary_key=True)
    file_size = db.Column(db.String(20), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    folder_name = db.Column(db.String(20), nullable=False)
    
    channel_length = db.Column(db.Integer, nullable=False)
    user_length = db.Column(db.Integer, nullable=False)

    uploaded_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    preferences = db.relationship('SNAPreferences', backref='fileinfo', lazy=True)


class FileInfoQuery():
    fileinfo = None
    def __init__(self, user_id, file_size, channel_length, user_length) -> None:
        self.fileinfo = FileInfo(user_id=user_id, file_size=file_size, channel_length=channel_length, user_length=user_length)
    
    def save_fileinfo(self):
        db.session.add(self.fileinfo)
        db.session.commit()
    
    @staticmethod
    def update_is_deleted(folder_name):
        # db.session.
        pass

    @staticmethod
    def find_avg_channel_length():
        pass

    @staticmethod
    def find_avg_user_length():
        pass
    