import datetime
import src.models.DB as DB
import src.models.FileInfos

from flask import current_app as app


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
        """
        if type(metric_id) is not int or type(layout_id) is not int or type(file_id) is not int:
            raise TypeError
        
        if metric_id < 0 or metric_id >= len(app.config["METRIC"]):
            raise ValueError("The value must be greater than 0 and less than the initial METRIC size")
        
        if layout_id >= 0 and layout_id < len(app.config["LAYOUT"]):
            raise ValueError("The value must be greater than or equal to 0 and less than the initial METRIC size")
        """
        self.sna = SNAPreferences(metric_id = metric_id, layout_id = layout_id, file_id = file_id)
    
    def save_sna(self) -> int:
        db.session.add(self.sna)
        db.session.commit()
        return self.sna.id
        

    @staticmethod
    def find_rate(which="metric") -> dict:
        which_as_class = SNAPreferences.metric_id if which == "metric" else SNAPreferences.layout_id
        return dict(db.session.query(which_as_class, db.func.count(which_as_class)).group_by(which_as_class).all())
    
    @staticmethod
    def find_total_count() -> int:
        return db.session.query(SNAPreferences).count()
