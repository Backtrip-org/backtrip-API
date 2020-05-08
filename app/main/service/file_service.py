import os
import uuid

from flask import send_from_directory
from werkzeug.utils import secure_filename

from ..util.exception.GlobalException import FileNotFoundException

DIRECTORY_PATH = os.getenv('FILES_DIRECTORY')

def upload(files):
    if 'file' not in files:
        raise FileNotFoundException()

    if not os.path.exists(DIRECTORY_PATH):
        os.mkdir(DIRECTORY_PATH)

    file = files.get('file')
    filename = secure_filename(str(uuid.uuid4()) + '.' + file.filename.split('.')[-1])
    file.save(os.path.join(DIRECTORY_PATH, filename))

    return filename

def download(filename):
    return send_from_directory(directory=DIRECTORY_PATH, filename=filename)
