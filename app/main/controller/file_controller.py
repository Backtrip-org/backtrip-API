import os
from flask import request, jsonify
from flask_restplus import Namespace, Resource
import uuid

from werkzeug.utils import secure_filename

from util.decorator import token_required

api = Namespace('file', description='files related operations')

DIRECTORY_PATH = 'files/'

@api.route('/upload')
class Upload(Resource):
    @api.doc('Upload a file')
    @api.response(201, 'Upload successful.')
    @api.response(400, 'File to upload is missing')
    @token_required
    def post(self):
        if 'file' not in request.files:
            api.abort(400, "File to upload is missing")

        if not os.path.exists(DIRECTORY_PATH):
            os.mkdir(DIRECTORY_PATH)

        file = request.files.get('file')
        filename = secure_filename(str(uuid.uuid4()) + '.' + file.filename.split('.')[-1])
        file.save(os.path.join(DIRECTORY_PATH, filename))

        return {'filename': filename}, 201
