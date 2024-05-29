class Message:
    def __init__(self, data):
        self.__data = data
    
    @classmethod
    def from_json(cls, json_data):
        return cls(data=json_data)
        
    def to_json(self,):
        return {'data': self.__data}


message  = Message('teste')
print(message)