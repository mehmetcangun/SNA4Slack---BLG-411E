import src.models.DB as DB
import src.models.FileInfos as fi

db = DB.db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(20), nullable=False)
    device_type = db.Column(db.String(255), nullable=False)
    
    files = db.relationship('FileInfo', backref='user', lazy=True, cascade="all,delete")

class UserQuery():
    user = None
    def __init__(self, ip_address=None, device_type=None) -> None:
        if not ip_address:
            raise ValueError("IP address is not found.")
        if not device_type:
            raise ValueError("Device Type is not found.")
        self.user = User(ip_address = ip_address, device_type = device_type)
    
    def insert(self) -> int:
        db.session.add(self.user)
        db.session.commit()
        return self.user.id

    @staticmethod
    def find_user_count() -> int:
        return db.session.query(User).count()
    
    @staticmethod
    def find_user_count_having_files() -> int:
        return db.session.query(User).join(fi.FileInfo).distinct().count()

    