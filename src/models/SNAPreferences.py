import datetime
from os import stat
import src.models.DB as DB
import src.models.FileInfo

db = DB.db
class SNAPreferences(db.Model):
    __tablename__ = "snapreferences"

    id = db.Column(db.Integer, primary_key=True)
    metric_id = db.Column(db.Integer, nullable=False)
    layout_id = db.Column(db.Integer, nullable=False)
    processed_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    file_id = db.Column(db.Integer, db.ForeignKey('fileinfo.id'), nullable=False)

class SNAPreferencesQuery():
    sna = None
    
    def __init__(self, metric_id, layout_id, file_id) -> None:
        self.sna = SNAPreferences(metric_id = metric_id, layout_id = layout_id, file_id=file_id)
    
    def save_sna(self) -> int:
        db.session.add(self.sna)
        db.session.commit()
        

    @staticmethod
    def find_rate(which="metric") -> dict:
        which_as_class = SNAPreferences.metric_id if which == "metric" else SNAPreferences.layout_id
        return dict(db.session.query(which_as_class, db.func.count(which_as_class)).group_by(which_as_class).all())
    
    @staticmethod
    def find_total_count() -> int:
        return db.session.query(SNAPreferences).count()
