import src.models.SNAPreference as sna_pref
from flask import current_app as app

def get_rate(which):
    rate_list = sna_pref.SNAPreferencesQuery.find_rate(which)
    total_sna_count = sna_pref.SNAPreferencesQuery.find_total_count() 
    which_full_list = app.config[str(which).upper()]
    labels = []
    data = []
    ids=[]
    for key in which_full_list:
        result_key =  0 if rate_list.get(key) is None else rate_list.get(key)/total_sna_count
        labels.append(which_full_list[key])
        data.append(result_key)
        ids.append(key)

    return labels, data, ids

def save_sna(layout_id, metric_id, file_id):
    return sna_pref.SNAPreferencesQuery(layout_id=layout_id, metric_id=metric_id, file_id=file_id).save_sna()
