from flask import request,g
from rmon.common.rest import RestView
from rmon.models import Server,ServerSchema
import json

class ServerList(RestView):
	"""
	redis server ServerList
	"""
	def get(self):
		"""get list"""
		servers =Server.query.all()
		return ServerSchema().dump(servers,many=True).data
	def post(self):
		"""create server"""
		data = request.get_json()
		server,errors = ServerSchema().load(data)
		if errors:
			return errors,400
		server.ping()
		server.save()
		return {'ok':True},201

class ServerDetail(RestView):
	method_decorators = (ObjectMustBeExist(Server),)
	def get(self,object_id):
		data, _ =ServerSchema().dump(g.instance)
		return data
	def put(self,object_id):
		schema = ServerSchema(context={'instance':g.instance})
		data = request.get_json()
		server,errors=schema.load(data,partial=True)
		if errors:
			return errors,400
		server.save()
		return {'ok':True}
	def delete(self,object_id):
		g.instance.delete()
		return {'ok':True},204

class ServerMetric(RestView):
	def get(self,object_id):
		server = Server.query.filter_by('id'=object_id).first()
		data = ServerSchema().dump(server).data
		return json.dumps(data.get_metrics())