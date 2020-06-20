from flask import request
from flask_restplus import Resource

from ..model.file.file_type import FileType
from ..util.dto import FileDto
from ..util.decorator import token_required
from ..util.exception.FileException import UploadFileNotFoundException, UnknownFileTypeException
from ..service.file_service import upload, download

api = FileDto.api
_file = FileDto.file


@api.route('/upload/<file_type>')
@api.param('file_type', 'Type of the file : Document or Photo')
class Upload(Resource):
    @api.doc('Upload a file')
    @api.response(201, 'Upload successful.')
    @api.response(400, 'File to upload is missing')
    @api.response(400, 'File type is unknown')
    @api.marshal_with(_file)
    @token_required
    def post(self, file_type):
        try:
            return upload(request.files, FileType.from_string(file_type)), 201
        except UploadFileNotFoundException as e:
            api.abort(400, e.value)
        except UnknownFileTypeException(file_type) as e:
            api.abort(400, e.value)


@api.route('/download/<file_id>')
@api.param('file_id', 'Id of the file to upload')
class Download(Resource):
    @api.doc('Download a file')
    @api.response(404, 'File not found')
    @token_required
    def get(self, file_id):
        return download(file_id)
