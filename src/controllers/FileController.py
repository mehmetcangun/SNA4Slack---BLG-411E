import os
import json

from flask import current_app as app, session
from zipfile import ZipFile

import src.models.FileInfos as fi

def save_fileinfo(user_id, file_size, channel_length, user_length, folder_name):
    return fi.FileInfoQuery(user_id=user_id, file_size=file_size, channel_length=channel_length, user_length=user_length, folder_name=folder_name).save_fileinfo()

def get_length(foldername, type):
    list_f = open(os.path.join(app.config['UPLOAD_FOLDER'], foldername, "extract", type))
    list_p = json.load(list_f)
    return len(list_p)

def extract_file():

    folder_name = session.get("current_foldername")

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, "file.zip")
    extract_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, "extract")
    
    with ZipFile(file_path , 'r') as zip:

        file_list = zip.namelist()
        sub_list_file = ['integration_logs.json', 'users.json', 'channels.json']

        if all(x in file_list for x in sub_list_file) and any('/' in string for string in file_list):
            zip.extractall(extract_path)
            return True
        else:
            return False

def update_is_deleted(folder_name) -> bool:
    return fi.FileInfoQuery.update_is_deleted(folder_name)

def get_avg_channel_length_in_files() -> float:
    return fi.FileInfoQuery.find_avg_channel_length_in_files()

def get_avg_user_length_in_files() -> float:
    return fi.FileInfoQuery.get_avg_user_length_in_files()