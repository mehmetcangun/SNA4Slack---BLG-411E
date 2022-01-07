import datetime
from itertools import count

import src.models.DB as DB
import src.models.User
import src.models.SNAPreferences

db = DB.db
class FileInfo(db.Model):
    __tablename__ = "fileinfo"

    id = db.Column(db.Integer, primary_key=True)
    file_size = db.Column(db.String(20), nullable=False)
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
    folder_name = db.Column(db.String(32), nullable=False)
    
    channel_length = db.Column(db.Integer, nullable=False)
    user_length = db.Column(db.Integer, nullable=False)

    uploaded_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    preferences = db.relationship('SNAPreferences', backref='fileinfo', lazy=True, cascade="all,delete")


class FileInfoQuery():
    fileinfo = None
    def __init__(self, user_id, file_size, channel_length, user_length, folder_name) -> None:
        self.fileinfo = FileInfo(user_id=user_id, file_size=file_size, channel_length=channel_length, user_length=user_length, folder_name=folder_name)
    
    def save_fileinfo(self)->int:
        db.session.add(self.fileinfo)
        db.session.commit()
        return self.fileinfo.id
    
    @staticmethod
    def update_is_deleted(folder_name) -> bool:
        file = FileInfo.query.filter_by(folder_name=folder_name).first()
        file.is_deleted = True
        db.session.commit()
        file = FileInfo.query.filter_by(folder_name=folder_name).first()
        return file.is_deleted

    @staticmethod
    def find_avg_channel_length_in_files() -> float:
        res = db.session.query(db.func.sum(FileInfo.channel_length), db.func.count(FileInfo.id)).all()[0]
        sum, count = res[0], res[1]
        return sum/count

    @staticmethod
    def get_avg_user_length_in_files() -> float:
        res = db.session.query(db.func.sum(FileInfo.user_length), db.func.count(FileInfo.id)).all()[0]
        sum, count = res[0], res[1]
        return sum/count
    