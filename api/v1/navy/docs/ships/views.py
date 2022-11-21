from flask_restx import Namespace, Resource, fields

ship_namespace = Namespace("Ships", path="/",description="Ships related operations")
