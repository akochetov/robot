import json

class Cfg:
    class __Cfg:
	settings = None
        def __init__(self):
		with open('/share/robot/config.json') as f:
			self.settings = json.load(f)
	
	def get(self, name):
		return self.settings[name]

    instance = None
    def __init__(self):
        if not Cfg.instance:
            Cfg.instance = Cfg.__Cfg()
    def get(self, name):
        return Cfg.instance.get(name)


