import os
import uuid

from flask import send_from_directory
from werkzeug.utils import secure_filename

from app.main import db
from app.main.model.file import File
from util.exception.FileException import UploadFileNotFoundException, IdFileNotFoundException

DIRECTORY_PATH = os.getenv('FILES_DIRECTORY')

def upload(files):
    if 'file' not in files:
        raise UploadFileNotFoundException()

    if not os.path.exists(DIRECTORY_PATH):
        os.mkdir(DIRECTORY_PATH)

    file = files.get('file')

    file_id = str(uuid.uuid4())
    file_extension = file.filename.split('.')[-1]
    file_name = ' '.join(file.filename.split('.')[0:-1])

    new_file = File(
        id=file_id,
        name=file_name,
        extension=file_extension
    )

    saved_file_name = secure_filename(file_id + '.' + file_extension)
    file.save(os.path.join(DIRECTORY_PATH, saved_file_name))

    db_save(new_file)

    return new_file

def download(file_id):
    file = File.query.filter_by(id=file_id).first()
    if not file:
        raise IdFileNotFoundException(file_id)

    filename = file.id + '.' + file.extension
    document = send_from_directory(directory=DIRECTORY_PATH, filename=filename)

    document.headers.add('id', file.id)
    document.headers.add('name', file.name)
    document.headers.add('extension', file.extension)

    return document


def db_save(file):
    db.session.add(file)
    db.session.commit()
