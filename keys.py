import json
import paths


class ObKeys:
    _instance = None
    _keys_dict = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            with open(paths.KEYS_FILE) as fp:
                cls._keys_dict = json.load(fp)
        return cls._instance
    
    def __getattr__(self, name):
        if name in self._keys_dict:
            return self._keys_dict[name]
        raise AttributeError(f"Key {name} not found.")
            
    def __setattr__(self, _name, _value):
        raise TypeError(f"Cannot edit keys after load.")