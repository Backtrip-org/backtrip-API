from flask import request
from flask_restplus import Namespace, Resource

from util.dto import FileDto
from ..util.decorator import token_required
from ..util.exception.GlobalException import FileNotFoundException
from ..service.file_service import upload, download

api = FileDto.api
_file = FileDto.file

@api.route('/upload')
class Upload(Resource):
    @api.doc('Upload a file')
    @api.response(201, 'Upload successful.')
    @api.response(400, 'File to upload is missing')
    @api.marshal_with(_file)
    @token_required
    def post(self):
        try:
            return upload(request.files), 201
        except FileNotFoundException as e:
            api.abort(400, e.value)


@api.route('/download/<filename>')
@api.param('filename', 'Name of the file to upload')
class Download(Resource):
    @api.doc('Download a file')
    @api.response(404, 'File not found')
    @token_required
    def get(self, filename):
        return download(filename)
