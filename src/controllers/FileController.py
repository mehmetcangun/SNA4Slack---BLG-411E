from ..models.FileInfo import FileInfoQuery
from flask import current_app as app, session
from zipfile import ZipFile
import os

def save_fileinfo(user_id, file_size, is_proper):
    return FileInfoQuery(user_id=user_id, file_size=file_size, is_proper=is_proper)

def extract_file():

    folder_name = session.get("current_foldername")

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, "file.zip")
    extract_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name, "extract")
    
    with ZipFile(file_path , 'r') as zip:
        # printing all the contents of the zip file
        #zip.printdir()

        file_list = zip.namelist()
        sub_list_file = ['integration_logs.json', 'users.json', 'channels.json']

        if all(x in file_list for x in sub_list_file) and any('/' in string for string in file_list):

            # extracting all the files
            print('Extracting all the files now...')
            zip.extractall(extract_path)
            print('Done!')
            return True
        else:
            return False
