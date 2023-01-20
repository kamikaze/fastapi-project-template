import base64
import json
import logging
from datetime import datetime, date
from socket import socket


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, date):
            return o.isoformat()
        elif isinstance(o, bytes):
            return base64.b64encode(o).decode('ascii')
        elif isinstance(o, socket):
            return str(o)
        elif isinstance(o, type):
            return str(o)

        return json.JSONEncoder.default(self, o)


class JSONFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps(record.__dict__, cls=CustomJSONEncoder)
