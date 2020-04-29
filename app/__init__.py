# app/__init__.py

from flask_restplus import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.trip_controller import api as trip_ns
from .main.controller.chat_message_controller import api as chat_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='BACKTRIP API',
          version='1.0',
          description='backtrip restfull api'
          )

api.add_namespace(user_ns, path='/user')
api.add_namespace(trip_ns, path='/trip')
api.add_namespace(chat_ns, path='/chat_message')
api.add_namespace(auth_ns)
