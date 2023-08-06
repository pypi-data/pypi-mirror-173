class DictClass:
    def __init__(self, dict_data):
        self.dict_data = dict_data
        for key, value in dict_data.items():
            if type(value) == dict:
                setattr(self, key, DictClass(value))
            else:
                setattr(self, key, value)
    def __repr__(self) -> str:
        return self.dict_data.__repr__()