from ..models.SNAPreferences import SNAPreferencesQuery
from flask import current_app as app

def get_rate(which):
    rate_list = SNAPreferencesQuery.find_rate(which)
    total_sna_count = SNAPreferencesQuery.find_total_count() 
    which_full_list = app.config[str(which).upper()]
    result = dict()
    for key in which_full_list:
        result[key] =  0 if rate_list.get(key) is None else rate_list.get(key)/total_sna_count
    return result

def save_sna(layout_id, metric_id, file_id):
    return SNAPreferencesQuery(layout_id=layout_id, metric_id=metric_id, file_id=file_id).save_sna()
