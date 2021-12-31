from ..models.FileInfo import FileInfoQuery
from flask import current_app as app

def save_fileinfo(user_id, file_size, is_proper):
    return FileInfoQuery(user_id=user_id, file_size=file_size, is_proper=is_proper)

