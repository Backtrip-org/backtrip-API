from flask import request
from flask_restplus import Resource

from ..util.dto import FileDto
from ..util.decorator import token_required
from ..util.exception.FileException import UploadFileNotFoundException
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
        except UploadFileNotFoundException as e:
            api.abort(400, e.value)


@api.route('/download/<file_id>')
@api.param('file_id', 'Id of the file to upload')
class Download(Resource):
    @api.doc('Download a file')
    @api.response(404, 'File not found')
    @token_required
    def get(self, file_id):
        return download(file_id)
