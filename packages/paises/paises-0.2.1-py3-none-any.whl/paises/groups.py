import json
import importlib.resources

class Groups(list):
	
	names = []

	def __init__(self):
		self.load_groups()
		if len(self) == 0:
			pass

	def load_groups(self):
				
		for i in importlib.resources.path(__package__, "groups").iterdir():			
			data = json.load(i.open(encoding='utf-8'))
			self.append(data)
			self.names.append(data['acronym'])
	
	def get_group(self, group):
		for g in self:
			if g['acronym'] == group:
				return g
			
