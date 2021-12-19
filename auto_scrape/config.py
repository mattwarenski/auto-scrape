import json

def load_config(file_path):
    with open(file_path, 'r') as file_raw:
        config_dict = json.loads(file_raw.read())
        return Config(config_dict)

class Config:
    def __init__(self, config_dict):
            self.config =  config_dict

    def get(self, prop, default=None):
        if prop in self.config:
            return self.config[prop]
        if default:
            return default
        raise Exception(f'Required prop not found: {prop}')

    def get_string(self, prop, default=None):
        raw = self.get(prop, default=default)
        return str(raw)

    def get_int(self, prop, default=None):
        raw = self.get(prop, default=default)
        return int(raw)

    def get_float(self, prop, default=None):
        raw = self.get(prop, default=default)
        return float(raw)
