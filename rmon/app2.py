import os
from flask import Flask
import json
def create_app():
	app = Flask('rmon')
	file=os.environ.get('RMON_CONFIG')
	file1=open('test.json','w')
	with open(file) as json_data:
		for each in json_data:
			if each.strip()[0]!='#':
				file1.write(each)
	file1.close()
	with open('test.json') as json_data2:
		data=json.load(json_data2)
	for key in data:
		app.config[key.upper()] = data.get(key)
	return app
		